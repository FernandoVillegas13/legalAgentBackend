from twilio.rest import Client
from dotenv import load_dotenv
import os

class Twilio:
    def __init__(self):
        load_dotenv()
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_FROM_NUMBER")
        self.to_number = os.getenv("TWILIO_TO_NUMBER")
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, message: str, media_url: str):
        self.client.messages.create(
            to=self.to_number,
            from_=self.from_number,
            body=message,
            media_url=[media_url]
        )