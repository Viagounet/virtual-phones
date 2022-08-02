# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

def send_sms_to(content, recipient, sender):
    account_sid = "AC4a7aa2d19b70231dd86c1c058c83acf8"
    auth_token = "15acb30062b35869098a92eb3513fe8b"

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=content,
                         from_=sender,
                         to=recipient
                     )
