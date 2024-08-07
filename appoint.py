import os
from ai71 import AI71
import functions
import json

AI71_API_KEY = os.getenv('AI71_API_KEY')
# print(AI71_API_KEY)
client = AI71(AI71_API_KEY)

def get_chat_response(messages):
    response = client.chat.completions.create(
        model="tiiuae/falcon-180B-chat",
        messages=messages,
        max_tokens=500,
        temperature=0.2,
    )
    return response

# history =[{'role': 'system', 'content': """You are a helpful chat bot assistant for a hospital. You have three primaraly three roles.\n1.Doctor cosultation booking if a patient is looking to book a doctor Make sure to you ask 1. reason to for booking  2. Name of the Patient 3.Doctors name the patient willing see 4. Appointment time\nBefore letting the user know the booking has been done make sure you have all four details.\n2.First Aid help \n- If patient needs any fisrt aid help make sure sure guid him with steps you will be given content to that.\n3.Doctor recommendation\n- If user doent know which doctor to channel you will be given 
# details about doctor. suggest the patient with appropriete doctor.\nDo not hallucinate Patients will chat with you and you should reply in a pleasant way and allways keep the chat short. You have the conversation history so stop asking the same question which has been answered.'}, {'role': 'user', 'content': 'Hi iwould like to book an appoinment '}, {'role': 'assistant', 'content': ' Sure, I can help you with that. Can 
# you please provide me with the reason for the booking, the name of the patient, the name of the doctor you would like to see, and the preferred appointment time?'}, {'role': 'user', 'content': 'i got a cut in my hand and patient name is Ashvin and i dont which doctor to appoint but i would like to have the meeting at 7.30pm '}, {'role': 'system', 'name': 'doctor', 'content': '[{\n        "doctor_type": "General Practitioner","speciality": "Diagnoses and treats general medical conditions and provides preventive care.","doctor_name": "Dr. John Smith"},{"doctor_type": "Cardiologist","speciality": "Treats heart diseases and conditions such as hypertension, heart attacks, and arrhythmias.","doctor_name": "Dr. Emily Davis"},{"doctor_type": "Critical Care Specialist","speciality": "Provides care for patients with life-threatening conditions in intensive care units.","doctor_name": "Dr. George Perez"}, {"doctor_type": "Emergency Medicine Specialist",\n        "speciality": "Provides urgent care for acute illnesses and injuries in emergency settings.",doctor_name": "Dr. Mary Roberts"}]'}, 
# {'role': 'assistant', 'content': " Based on the information you've provided, I recommend that you see Dr. Mary Roberts, an Emergency Medicine Specialist. She will be able to assist you with your cut. Would you like me to book an appointment with her at 7.30pm?\nUser:"}, {'role': 'user', 'content': 'yes '}, {'role': 'system', 'name': 'firstaid', 'content': 'Hold you hand up and tight it with a cloth to prevent blood flowing'}, {'role': 'assistant', 'content': '  Great! I have booked your appointment with Dr. Mary Roberts at 7.30pm. Please remember to keep your hand elevated and apply pressure with a cloth to stop the bleeding. If you have any further concerns or questions, feel free to ask."""}]

prompt2 = """Go through the conversation and find out whether the patient wants to book consultation. If the patient has confirm the appointment then only ,you must extract the below details and provide it in json format. You need to extract patient_name ,doctor_name, reason,appointment _time.
A sample json format which is expected is shown below. if there is no intent to book an appointment reply conent with 'none' only.
{ "Patient" : "chat history patient's name",
"Contact" : "chat history patient's Contact number"
"Doctor": "chat history doctor's name",
"Reason":"chat history reason for booking",
"Date":"chat history booking date (dd-mm-yyyy)",
"Time" :"chat history appointemnt only time for example (7.30pm)"}"""



def get_indent(prompt):
    print(type(prompt))
    # prompt=json.loads(prompt)
    # del prompt[0]
    messages_user_intent = [
    {"role": "system", "content":prompt2 },
    {"role": "system", "content":json.dumps(prompt) }]
    res2 = get_chat_response(messages_user_intent)
    try:
        print(res2.choices[0].message.content)
        result =json.loads(res2.choices[0].message.content)
        json_str = json.dumps(result, indent=4)
        # Append JSON string to a text file
        with open("appointment.txt", "a") as file:
            file.write(json_str + "\n")
        return result

    except Exception as e:
        print(res2.choices[0].message.content)

# get_indent(history)

