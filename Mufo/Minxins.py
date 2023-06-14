
from . import settings

import requests

def send_otp_on_phone(mobile_number, otp):
    API_KEY = settings.API_KEY
    SENDER_ID = settings.SENDER_ID
    ROUTE = settings.ROUTE
    Templte_id =  settings.Templte_id

    url = "https://control.msg91.com/api/v5/otp"
    headers = {
        "Content-Type": "application/json",
        "authkey": API_KEY
    }
    payload = {
        "template_id": Templte_id ,  
        "mobile": mobile_number,
        "OTP": otp,
        "sender": SENDER_ID,
        "route": ROUTE
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response)
    if response.status_code == 200:
        # OTP sent successfully
        return True
    else:
        # Failed to send OTP
        return False