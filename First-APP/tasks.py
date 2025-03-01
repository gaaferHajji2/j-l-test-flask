from dotenv import load_dotenv

import os

import requests

load_dotenv()

def send_simple_message(to, subject, message):
    API_KEY= os.getenv('API_KEY')
    DOMAIN_NAME = os.getenv('DOMAIN_NAME')
    try:
        request_data = requests.post(
                f"https://api.mailgun.net/v3/{DOMAIN_NAME}/messages",
                auth=("api", f"{API_KEY}"),
                data={
                    "from": f"Jafar Hajji <mailgun@{DOMAIN_NAME}>",
                    "to": [to, f"YOU@{DOMAIN_NAME}"],
                    "subject": subject,
                    "text": message
                },
                
            )

        print(request_data)
        print(request_data.json())
    except Exception as e:
        print(e.__str__())