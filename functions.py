from firstaid import qna_bot

def first_aid(query):
    # response = qna_bot(query)
    return 'keep ice'

def doctor_details(input):
    return """[{
        "doctor_type": "General Practitioner",
        "speciality": "Diagnoses and treats general medical conditions and provides preventive care.",
        "doctor_name": "Dr. John Smith"},
    {
        "doctor_type": "Cardiologist",
        "speciality": "Treats heart diseases and conditions such as hypertension, heart attacks, and arrhythmias.",
        "doctor_name": "Dr. Emily Davis"
    },
    {
        "doctor_type": "Critical Care Specialist",
        "speciality": "Provides care for patients with life-threatening conditions in intensive care units.",
        "doctor_name": "Dr. George Perez"
    },
    {
        "doctor_type": "Emergency Medicine Specialist",
        "speciality": "Provides urgent care for acute illnesses and injuries in emergency settings.",
        "doctor_name": "Dr. Mary Roberts"
    }
]"""




