import streamlit as st
import os
from ai71 import AI71
import functions
import datetime
from appoint import get_indent


current_datetime = datetime.date.today()
day_of_week = current_datetime.strftime("%A")

AI71_API_KEY = st.secrets["AI71_API_KEY"]
# print(AI71_API_KEY)
client = AI71(AI71_API_KEY)


available_functions = {
    "firstaid": functions.first_aid,
    "doctor": functions.doctor_details,
}

def get_chat_response(messages):
    response = client.chat.completions.create(
        model="tiiuae/falcon-180B-chat",
        messages=messages,
        max_tokens=500,
        temperature=0.4,
    )
    return response

def get_chat_response_decide(messages):
    response = client.chat.completions.create(
        model="tiiuae/falcon-180B-chat",
        messages=messages,
        max_tokens=100,
        temperature=0.2,
    )
    return response

def update_decide(msg):
    messages_decide = [
        {"role": "system", "content": """You are a helpful assistant. You will be given a chat history. Examine the last user message and categorize it into one of three options: 'firstaid', 'doctor', or 'none'. Return only the category word without any additional text or spaces.
Categorization criteria:

'firstaid': ONLY if the message explicitly requests immediate first aid help or instructions.
'doctor': ONLY if the message specifically asks for a doctor recommendation.
'none': For any message that doesn't fit the above categories.

Rules:

Do not assume 'firstaid' for normal regular check-ups.
Only return 'firstaid', 'doctor', or 'none' without spaces or additional text.
If you can't categorize the message into 'firstaid' or 'doctor', return 'none'.
Do not provide explanations or additional information.
Do not make assumptions or inferences beyond what is explicitly stated in the message."""},
        {"role": "user", "content": f"{msg}"},
    ]
    return messages_decide

def update_message_user(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

def models_response(user_history, msg):
    decide = update_decide(msg)
    res = get_chat_response_decide(decide)
    response = res.choices[0].message.content.lower().replace(" ", "")
    
    if response == "none":
        user_history = update_message_user(user_history, "user", msg)
        res2 = get_chat_response(user_history)
        update_message_user(user_history, "assistant", res2.choices[0].message.content)
        return user_history, res2.choices[0].message.content
    else:
        if response not in available_functions:
            print(response)
            return user_history, "Feature not available"
        else:
            function_to_call = available_functions[response]
            function_response = function_to_call(msg)
            user_history = update_message_user(user_history, "user", msg)
            user_history.append({"role": "system", "name": f"{response}", "content": f"{function_response}"})
            res2 = get_chat_response(user_history)
            update_message_user(user_history, "assistant", res2.choices[0].message.content)
            return user_history, res2.choices[0].message.content
promt =f"""You are a helpful chatbot assistant for a hospital with three primary roles:

Initial Inquiry:

Ask if the patient needs emergency assistance or wants to book a regular check-up.
Role 1: Doctor Consultation Booking:
    If a patient wants to book a doctor's appointment,you MUST collect the following information in order:
    a. Reason for booking
    b. Patient's full name
    c. Contact number
    d. Preferred doctor's name
    e. Preferred appointment date and time
    After collecting all details,you MUST summarize and ask the patient to confirm:
    "Please confirm the following details:
    -Name: [PATIENT NAME]
    -Contact Number:[PATIENT CONTACT NUMBER]
    -Reason for Visit: [PATIENT REASON FOR VISIT]
    -Doctor: [DOCTOR NAME]
    -Appointment Date: [APPOINTMENT DATE (dd-mm-yyy)]
    -Appointment Time : [APPOINTMENT TIME (hh:mm)]
    -Is this information correct?"
Important - if you havent collected the all these neccesary details for appointment make sure to ask again and again for those details.
Role 2: First Aid Guidance:

If a patient needs first aid help, provide step-by-step instructions based on the given content.
Emphasize that these are temporary measures and professional medical help should be sought if the condition is serious.

Role 3: Doctor Recommendation:

If a patient doesn't know which doctor to see, ask about their symptoms or medical concerns.
Based on the provided doctor details, suggest the most appropriate specialist.
Briefly explain why this doctor is recommended for their specific case.

General Guidelines:

Always identify the current date and day of the week at the beginning of the conversation: "Today is {current_datetime}, {day_of_week}."
Keep responses pleasant, concise, and to the point.
Utilize the conversation history to avoid repeating questions already answered.
Do not provide any information not explicitly given in your knowledge base.
If unsure about any medical advice, recommend the patient to consult with a healthcare professional.
For any non-medical queries, politely redirect the conversation to hospital-related matters.

Remember, you are not a substitute for professional medical advice, diagnosis, or treatment. In case of serious medical concerns, always advise patients to seek immediate professional medical attention.
Also, ensure that you keep your responses minimal but concise and precise. """
messages_user = [
    {"role": "system", "content":promt },
]



# prompt2 = """Go through the conversation and find out whether the patient wants to book consultation. If so, extract the below details and provide it in json format. You need to extract patient_name ,contact_No ,doctor_name, reason,appointment _Date and appointment_time.
# A sample json format which is expected is shown below. if there is no intent to book an appointment reply none.
# {"patient" : " from chat history patient's name",
# "contact_No" : " from chat history patient's contact number",
# "Doctor": "from chat history doctor's name",
# "Reason":"from chat history reason for booking",
# "Date":"from chat history appointment Date ",
# "time" :"chat history appointemnt time"}"""



def main():
    global messages_user
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'stop']:
            print("Assistant: Goodbye! Take care.")
            get_indent(messages_user)
            print(messages_user)
            break
        
        messages_user, response = models_response(messages_user, user_input)
        print("Assistant:", response)

if __name__ == "__main__":
    main()
