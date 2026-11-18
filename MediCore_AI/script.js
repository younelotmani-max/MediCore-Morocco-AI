const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const esc = t => String(t).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const statusClass = t => /^(CRITICAL)/.test(t) ? "c-crit" : /^(WARNING|URGENT)/.test(t) ? "c-warn" : /^MODERATE/.test(t) ? "c-mod" : "c-ok";

/* ---------- talk to server.py ---------- */
async function api(path, body) {
  const r = await fetch(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.error || "Server error.");
  return data;
}
const errText = e => e instanceof TypeError ? "Cannot reach the server. Run server.py, then open http://localhost:8000" : e.message;
const showErr = (el, e) => { el.innerHTML = `<p class="err">${esc(errText(e))}</p>`; };

/* ---------- navigation ---------- */
function go(id) {
  $$(".view").forEach(v => v.classList.toggle("on", v.id === id));
  $$("nav [data-go]").forEach(b => b.classList.toggle("act", b.dataset.go === id));
  scrollTo(0, 0);
  if (id !== "vault") lockVault();
}
document.addEventListener("click", e => {
  const b = e.target.closest("[data-go]");
  if (b) { e.preventDefault(); go(b.dataset.go); }
});

/* ---------- monitor reacts to the last patient ---------- */
function setBeat(hr) {
  $("#bpm").textContent = hr;
  document.documentElement.style.setProperty("--beat", (60 / Math.min(Math.max(hr, 30), 220)).toFixed(2) + "s");
}

/* ---------- 1. register patient ---------- */
$("#regForm").addEventListener("submit", async e => {
  e.preventDefault();
  const out = $("#regOut");
  const body = { name: $("#rName").value, age: $("#rAge").value, hr: $("#rHr").value, sugar: $("#rSug").value };
  try {
    const d = await api("/api/register", body);
    setBeat(d.hr);
    out.innerHTML = `<div class="card ${statusClass(d.status)}"><h3>${esc(d.status)}</h3><p>${esc(d.name || "Patient")}, ${d.age} years · ${d.hr} bpm · sugar ${d.sugar}</p></div>`;
    e.target.reset();
  } catch (err) { showErr(out, err.message.startsWith("invalid literal") ? new Error("Enter valid positive numbers only.") : err); }
});

/* ---------- 3. triage ---------- */
$("#triForm").addEventListener("submit", async e => {
  e.preventDefault();
  const out = $("#triOut");
  try {
    const d = await api("/api/triage", { name: $("#tName").value, symptom: $("#tSym").value });
    out.innerHTML = `<div class="card ${statusClass(d.department)} ${d.department.startsWith("CRITICAL") ? "cardio" : ""}"><h3>${esc(d.department)}</h3><p>Hello ${esc(d.name)}, your appointment is at ${esc(d.time)}. We wish you good health.</p></div>`;
    e.target.reset();
  } catch (err) { showErr(out, err); }
});

function lockVault() {
  $("#vaultBody").hidden = true; $("#vaultBody").innerHTML = "";
  $("#gate").hidden = false; $("#pw").value = ""; $("#gateMsg").textContent = "";
}

/* ---------- 4. admin vault (password checked by server.py) ---------- */
const table = (heads, rows) => rows.length
  ? `<div class="wrap"><table class="tbl"><tr>${heads.map(h => `<th>${h}</th>`).join("")}</tr>${rows.join("")}</table></div>`
  : '<p class="sub">Nothing here yet. Register a patient or run a triage to fill this list.</p>';
const pick = (r, ...keys) => esc(keys.map(k => r[k]).find(v => v !== undefined) ?? "");
$("#gate").addEventListener("submit", async e => {
  e.preventDefault();
  const msg = $("#gateMsg");
  try {
    const d = await api("/api/vault", { password: $("#pw").value });
    msg.textContent = "Access granted. Welcome, Director.";
    $("#gate").hidden = true;
    const pill = t => `<span class="pill ${statusClass(t)}">${esc(t)}</span>`;
    const st = r => r.status || r.statuts || "";
    const rank = r => st(r).startsWith("CRITICAL") ? 0 : 1;
    const watch = d.records.filter(r => /^(CRITICAL|WARNING)/.test(st(r))).sort((a, b) => rank(a) - rank(b));
    const alerts = watch.length
      ? `<div class="alerts">${watch.map(r => `<div class="alert ${rank(r) ? "warn" : ""}"><h4>${pick(r, "name") || "Unnamed"}</h4><p>${pick(r, "age")} years · ${pick(r, "heart_rate", "hr")} bpm · sugar ${pick(r, "sugar_level", "sugar")}</p>${pill(st(r))}</div>`).join("")}</div>`
      : '<p class="sub">No critical or warning patients right now.</p>';
    $("#vaultBody").innerHTML =
      "<h3>Critical scanner</h3>" + alerts +
      "<h3>Patient records</h3>" + table(["Name", "Age", "HR", "Sugar", "Status"],
        d.records.map(r => `<tr><td>${pick(r, "name")}</td><td>${pick(r, "age")}</td><td>${pick(r, "heart_rate", "hr")}</td><td>${pick(r, "sugar_level", "sugar")}</td><td>${pill(r.status || r.statuts || "")}</td></tr>`)) +
      "<h3>Appointments</h3>" + table(["Time", "Name", "Symptom", "Department"],
        d.triage.map(r => `<tr><td>${pick(r, "time")}</td><td>${pick(r, "name")}</td><td>${pick(r, "douleure", "symptom")}</td><td>${pill(r.department || r.dept || "")}</td></tr>`));
    $("#vaultBody").hidden = false;
  } catch (err) { msg.textContent = errText(err); }
});
