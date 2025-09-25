from django.conf import settings
import africastalking

def send_customer_sms(phone, message):
    try:
        username = getattr(settings, "AT_USERNAME", "sandbox")
        api_key = getattr(settings, "AT_API_KEY", "")
        sender = getattr(settings, "AT_SENDER_ID", "SENDER")
        if not api_key:
            print(f"[SMS MOCK] to {phone}: {message}")
            return
        africastalking.initialize(username=username, api_key=api_key)
        sms = africastalking.SMS
        sms.send(message, [phone], sender_id=sender)
    except Exception as e:
        print(f"[SMS ERROR] {e}")
