import streamlit as st
from datetime import datetime
from lab_radar import analyze_vitals
from triage_bot import detect_department

st.title(" MediCore Morocco AI - Web Portal ")
page = st.sidebar.selectbox("Choose Department:", ["1. AI Lab Radar", "2. Multilingual Triage Bot", "3. Admin Medical Vault"])
if page == "1. AI Lab Radar":
    st.header("Blood & Heart AI Analysis")
    name = st.text_input("Patient Name:")
    age = st.number_input("Patient Age:", min_value=1, max_value=120)
    heart_rate = st.number_input("Heart Rate (BPM):", min_value=1, max_value=300)
    sugar = st.number_input("Blood Sugar Level (mg/dL):", min_value=1, max_value=600)
    if st.button("Run AI Diagnosis"):
        status = analyze_vitals(heart_rate, sugar)
        st.subheader(f"Diagnosis Result: {status}")      
        file = open("medical_records.txt", "a")
        file.write(f"Name: {name} | Age: {age} | HR: {heart_rate} | Sugar: {sugar} | Status: {status}\n")
        file.close()
        st.success(" Patient record saved to Hospital Vault!")
elif page == "2. Multilingual Triage Bot":
     st.header(" Smart Emergency Triage (Darija / FR / EN / AR)")
     name = st.text_input("Your Name:")
     symptom = st.text_input("Describe what hurts you (ex: qlbi, rassi, heart, tete):")
     if st.button("Find My Doctor"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dept = detect_department(symptom)
        st.info(f" Patient: {name} |  Time: {now}")
        st.warning(f" Routing To: {dept}")
        
        log = open("triage_log.txt", "a", encoding="utf-8")
        log.write(f"Name: {name} | Time: {now} | Symptom: {symptom} | Dept: {dept}\n")
        log.close()
elif page == "3. Admin Medical Vault":
     st.header(" Director Secret Vault")
     pwd = st.text_input("Enter Admin Password:", type="password")  
     if st.button("Unlock Vault"):
        if pwd == "Kawal2009@":
            st.success("Access Granted! Welcome Director Younes")
            st.subheader(" Lab Records:")
            st.text(open("medical_records.txt", "r").read())
            st.subheader(" Triage Logs:")
            st.text(open("triage_log.txt", "r", encoding="utf-8").read())
        else:
            st.error(" ACCESS DENIED! Intruder Alert")   

