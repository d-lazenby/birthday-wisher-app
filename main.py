from datetime import datetime
from dotenv import load_dotenv
import os
import pandas as pd
import random
import smtplib

load_dotenv()

sender = os.getenv("SENDER_EMAIL")
recipient = os.getenv("RECIPIENT_EMAIL")
password = os.getenv("LOGIN_PASSWORD")

# Check if today is anyone's birthday
birthdays = pd.read_csv("birthdays.csv")
month, day = datetime.now().month, datetime.now().day
filtered_birthdays = birthdays[
    (birthdays['month'] == month) & (birthdays['day'] == day)
]

if not filtered_birthdays.empty:
    for i in range(filtered_birthdays.shape[0]):
        # Get name for each row in df and pick a template
        name = filtered_birthdays.iloc[i]["name"]
        letter_path = f"./letter_templates/letter_{random.randint(1, 3)}.txt"
        # Open file
        with open(letter_path, 'r') as f:
            letter_data = f.read()

        # Modifies birthday letter templates
        letter_data = letter_data.replace("[NAME]", name)
        
        # Send letter
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=sender, password=password)
                connection.sendmail(
                    from_addr=sender, 
                    to_addrs=recipient, 
                    msg=f"Subject:Happy Birthday!!!\n\n{letter_data}"
                    )
        except:
            print("Couldn't send email for some reason. Make sure to try again before tomorrow!")
        


