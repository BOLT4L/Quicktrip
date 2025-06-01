import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio configuration
TWILIO_ACCOUNT_SID = 'AC01fa514281e583e66f9d1fb293d6010f'
TWILIO_AUTH_TOKEN = '1fa05952205a1e544adefef74e7c3a53'
TWILIO_PHONE_NUMBER = '+12674122273'

def get_twilio_client():
    from twilio.rest import Client
    return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_twilio_message(to_number, message_body):
    try:
        client = get_twilio_client()
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return message.sid
    except Exception as e:
        print(f"Error sending message: {e}")
        return None 