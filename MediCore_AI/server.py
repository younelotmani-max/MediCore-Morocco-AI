"""Bridge between the web interface and the MediCore_AI Python code.
Run:  python server.py   then open  http://localhost:8000
Uses analyze_vitals (lab_radar.py) and detect_department (triage_bot.py) as they are.
"""
import hmac
import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from lab_radar import analyze_vitals
from triage_bot import detect_department

BASE = os.path.dirname(os.path.abspath(__file__))
RECORDS = os.path.join(BASE, "medical_records.txt")
TRIAGE = os.path.join(BASE, "triage_log.txt")
ADMIN_PASSWORD = "Kawal2009#@"

# only these 3 files + the img/ folder are served (never your .py or .txt files)
PAGES = {"/": "index.html", "/index.html": "index.html", "/style.css": "style.css", "/script.js": "script.js"}
TYPES = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8"}


def clean(text):
    """One line, no '|' so the txt format stays intact."""
    return " ".join(str(text).replace("|", " ").split())


def append_line(path, line):
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)


def parse_file(path):
    """Read a log file into a list of dicts (keys lowercased)."""
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if "|" not in line:
                continue
            row = {}
            for part in line.split("|"):
                if ":" in part:
                    key, value = part.split(":", 1)
                    row[key.strip().lower()] = value.strip()
            rows.append(row)
    return rows


class Handler(BaseHTTPRequestHandler):
    def reply(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?")[0]
        name = PAGES.get(path)
        if not name and path.startswith("/img/"):
            file = os.path.join("img", os.path.basename(path))  # basename: no path tricks
            if os.path.splitext(file)[1].lower() in TYPES and os.path.isfile(os.path.join(BASE, file)):
                name = file
        if not name:
            return self.reply(404, {"error": "Not found"})
        with open(os.path.join(BASE, name), "rb") as f:
            self.reply(200, f.read(), TYPES[os.path.splitext(name)[1].lower()])

    def do_POST(self):
        routes = {"/api/register": self.register, "/api/triage": self.triage, "/api/vault": self.vault}
        route = routes.get(self.path)
        if not route:
            return self.reply(404, {"error": "Not found"})
        try:
            size = int(self.headers.get("Content-Length", 0))
            code, payload = route(json.loads(self.rfile.read(size) or b"{}"))
        except (ValueError, TypeError):
            code, payload = 400, {"error": "Invalid request."}
        self.reply(code, payload)

    def register(self, data):
        name = clean(data.get("name", ""))
        age, hr, sugar = int(data["age"]), int(data["hr"]), int(data["sugar"])
        if age <= 0 or hr <= 0 or sugar <= 0:
            return 400, {"error": "Numbers must be positive!"}
        status = analyze_vitals(hr, sugar)
        append_line(RECORDS, f"Name : {name} | Age : {age} | HEART_RATE : {hr} | SUGAR_LEVEL : {sugar} | STATUS : {status}\n")
        return 200, {"status": status, "name": name, "age": age, "hr": hr, "sugar": sugar}

    def triage(self, data):
        name, symptom = clean(data.get("name", "")), clean(data.get("symptom", ""))
        if not name or not symptom:
            return 400, {"error": "Write your name and what you feel."}
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        department = detect_department(symptom)
        append_line(TRIAGE, f"Name : {name} | Time : {now} | Douleure : {symptom} | Department : {department} \n")
        return 200, {"department": department, "time": now, "name": name}

    def vault(self, data):
        if not hmac.compare_digest(str(data.get("password", "")).encode(), ADMIN_PASSWORD.encode()):
            return 401, {"error": "Access denied. Wrong password."}
        return 200, {"records": parse_file(RECORDS), "triage": parse_file(TRIAGE)}

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("Hospital OS is running on http://localhost:8000  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped.")
