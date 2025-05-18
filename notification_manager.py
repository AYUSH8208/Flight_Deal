from twilio.rest import Client
import os

class NotificationManager:
    def __init__(self):
        # Twilio credentials are loaded from environment variables, not hardcoded.
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_FROM_NUMBER')
        self.to_number = os.getenv('TWILIO_TO_NUMBER')

        if not account_sid or not auth_token:
            print("Warning: Twilio credentials (account_sid and auth_token) are not set in the environment variables. SMS notifications will be disabled.")
            self.client = None
        else:
            self.client = Client(account_sid, auth_token)

    def send_message(self, message):
        if not self.client:
            # Twilio not configured, do nothing
            return
        message = self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=self.to_number
        )
        print(message.sid)