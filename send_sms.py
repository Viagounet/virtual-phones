# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

def send_sms_to(content, recipient, sender):
    account_sid = "AC4a7aa2d19b70231dd86c1c058c83acf8"
    auth_token = "859b73c28fa476ab58c2d11b4ece6f80"
    print(f"Account_sid {account_sid}\nAuth_token {auth_token}"
          f"\nContent {content}\nRecipient {recipient}\nSender {sender}")
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=content,
                         from_=sender,
                         to=recipient
                     )
