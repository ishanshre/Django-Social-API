from accounts.tokens import encode_token

from django.urls import reverse
from django.core.mail import EmailMessage

def send_email(actual_url, username, to_email, action):
    if action == "email_verify":
        subject = "Verify your User Account"
        body = f'''
            Hello {username.title()}! Please open the link to verify your email
            {actual_url}
        '''
    if action == "password_reset":
        subject = "Reset Your Password"
        body = f'''
            Hello {username.title()}! Please open the link to reset your password
            {actual_url}
        '''
    email = EmailMessage(
        subject=subject,
        body=body,
        to=[to_email]
    )
    email.send()

def create_email(username, email, action, current_site):
    token = encode_token(username, action)
    if action == "email_verify":
        relative_path = reverse("accounts:email_verify")
    if action == "password_reset":
        relative_path = reverse("accounts:password_reset")
    actual_url = "http://"+current_site+relative_path+"?token="+str(token)
    send_email(actual_url=actual_url, username=username, to_email=email, action=action)

