import sqlite3

# conn = sqlite3.connect("appointment_DB.db", check_same_thread=False)
# c = conn.cursor()


def create_table():
    conn = sqlite3.connect("appointment_DB.db", check_same_thread=False)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS appointments
        ([Patient] TEXT , [Contact] INTEGER , [Reason] TEXT , [Doctor] TEXT, [Date] TEXT ,[Time] TEXT)
        """
    )
    conn.commit()
    conn.close()


def insert_data(data):
    conn = sqlite3.connect("appointment_DB.db", check_same_thread=False)
    c = conn.cursor()
    Patient = data["Patient"]
    Contact = int(data["Contact"])
    Doc = data["Doctor"]
    Reason = data["Reason"]
    Date = data["Date"]
    Time = data["Time"]
    c.execute(
        """
        INSERT INTO appointments (Patient, Contact, Reason, Doctor, Date, Time)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (Patient, Contact, Reason, Doc, Date, Time)
    )
    conn.commit()
    conn.close()

def retrieve_appointments():
    conn = sqlite3.connect("appointment_DB.db" , check_same_thread=False)
    c = conn.cursor()
    
    c.execute("SELECT * FROM appointments")
    
    appointments = c.fetchall()
    
    conn.close()
    
    return appointments

# Function to print appointments in a readable format
def print_appointments():
    appointments = retrieve_appointments()
    if not appointments:
        print("No appointments found.")
    else:
        for appointment in appointments:
            print(f"Patient: {appointment[0]}")
            print(f"Contact: {appointment[1]}")
            print(f"Reason: {appointment[2]}")
            print(f"Doctor: {appointment[3]}")
            print(f"Date: {appointment[4]}")
            print(f"Time: {appointment[5]}")
            print("-" * 20)  # Separator between appointments

# print_appointments()

# create_table()
# insert_data(data)

