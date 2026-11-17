from rich import print


def analyze_vitals(heart_rate: int, sugar: int) -> str:
    """AI Engine to calculate patient risk score"""
    risk_score = 0

    if heart_rate > 120 or heart_rate < 50:
        risk_score += 50

    if sugar > 200 or sugar < 70:
        risk_score += 50

    if risk_score >= 80:
        return "CRITICAL EMERGENCY"
    elif risk_score >= 40:
        return "WARNING - MONITOR"
    else:
        return "NORMAL & STABLE"


def register_patient():
    name = input("Your Name Please : ").strip()

    try:
        age = int(input("Your Age : "))
        heart_rate = int(input("Your heart rate : "))
        sugar = int(input("Your Blood sugar level : "))

        if age <= 0 or heart_rate <= 0 or sugar <= 0:
            raise ValueError("Numbers must be positive!")

        status = analyze_vitals(heart_rate, sugar)

        if status == "CRITICAL EMERGENCY":
            print(f"[bold red]Your result is : {status}")
        elif status == "WARNING - MONITOR":
            print(f"[bold yellow]Your result is : {status}")
        else:
            print(f"[bold green]Your result is : {status}")

        file = open(r"C:\Users\__uness\Documents\python\MediCore_AI\medical_records.txt", "a")
        file.write(f"Name : {name} | Age : {age} | HEART_RATE : {heart_rate} | SUGAR_LEVEL : {sugar} | STATUS : {status}\n")
        file.close()
    
    except ValueError:
        print("[bold red]INPUT ERROR: Please enter valid positive numbers only!")


def batch_critical_scanner():
    patients = ["Karim", "Salma", "Youssef", "Nadia"]
    scores = [20, 95, 45, 85]

    for patient, score in zip(patients, scores):
        print(f"{patient} : {score}")

    print(list(filter(lambda s: s >= 80, scores)))


#register_patient()
#batch_critical_scanner() : hada bla mat acctivih ok 