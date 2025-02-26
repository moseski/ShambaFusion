# email_utils.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_confirmation_email(to_email):
    message = Mail(
        # todo=> Create a shambafusion custom mail
        from_email='kimanimuiruri001@gmail.com',  
        to_emails=to_email,
        subject='Confirmation Email',
        html_content='<p>Thank you for signing up! Please confirm your email.</p>',
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return None
