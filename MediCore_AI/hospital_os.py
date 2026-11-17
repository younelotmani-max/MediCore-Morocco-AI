from lab_radar import register_patient, batch_critical_scanner
from triage_bot import start_triage
admin_password="Kawal2009#@"

def admin_hopital():
    password=input("Hello please write your password : ")
    print("-"*70)
    if password==admin_password:
        print("Access Granted Welcome Director")
        print("All Appointment and infos")
        radar_file=open(r"C:\Users\__uness\Documents\python\MediCore_AI\medical_records.txt", "r")
        print(radar_file.read())
        radar_file.close()
        print("-"*70)
        data_appointment=open(r"C:\Users\__uness\Documents\python\MediCore_AI\triage_log.txt", "r")
        print(data_appointment.read())
        data_appointment.close()
    else :
        print("ACCESS DENIED! Intruder Alert") 

def menu_hopital():
    while True:
        print("1. Register Patient & Lab Analysis\n2. Critical Batch Scanner\n3. Multilingual AI Triage\n4. Admin Medical Vault\n5. Exit")       
        choice=input("Please Choose the number that best fits your needs : ").strip()
        if choice=="1":
            register_patient()
        elif choice=="2":
            batch_critical_scanner()
        elif choice=="3":
            start_triage()
        elif choice=="4":
            admin_hopital()
        elif choice=="5" :
            print("Thank you for visiting Hospital_os . We wish you good health. Goodbye!")
            break
        else:
            print("Invalid choice Please select 1 to 5.")

menu_hopital()            




