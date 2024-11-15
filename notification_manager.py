from twilio.rest import Client

from dotenv import  load_dotenv
import  os
load_dotenv()
class NotificationManager:

    def __init__(self):
        self.client=Client(os.getenv('account_sid'),os.getenv('auth_token'))


    def send_message(self,message):
        message=self.client.messages .create(body=message,
                                             from_='+17866299455',
                                             to='+918208443163')
        print(message.sid)