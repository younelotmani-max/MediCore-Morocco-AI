from rich import print
from datetime import datetime

def detect_department(symptom: str) -> str:

    """AI Triage Bot to route patients by symptoms"""
    symptom = symptom.lower()
    if "qalbi" in symptom or "heart" in symptom or "coeur" in symptom or "قلب" in symptom :
        return "CRITICAL - CARDIOLOGY DEPARTMENT"
    
    elif "rassi"in symptom or "head"in symptom or "tete" in symptom or "skhana" in symptom or "fever" in symptom:
        return "URGENT - NEUROLOGY & FEVER UNIT"
    
    elif "kerchi" in symptom or "stomach" in symptom or "ventre" in symptom or "معدة" in symptom : 
        return "MODERATE - GASTROENTEROLOGY UNIT"
    else :
         return"NORMAL - GENERAL CONSULTATION"

def start_triage():
    name=input("Print your name : ").strip()
    print("Describe your symptoms (Darija / FR / EN / AR): ")
    symptom=input("Write what you feel : ")
    now= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    department=detect_department(symptom)
    print(f"Hello {name} this is your tiket , your Appointment in {now} and your Department in {department} We wish you good health ")
    data_appointment=open(r"C:\Users\__uness\Documents\python\MediCore_AI\triage_log.txt", "a")
    data_appointment.write(f"Name : {name} | Time : {now} | Douleure : {symptom} | Department : {department} \n")
    data_appointment.close()

#start_triage()    