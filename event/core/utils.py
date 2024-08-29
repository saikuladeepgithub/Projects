

from django.core.mail import send_mail
from django.conf import settings

def send_registration_success_email(user_email, username):
    subject = "Successfully Registered on Techies Event Management"
    message = f"Hi {username},\n\nYou have successfully registered on Techies Event Management.\nIf you need any further assistance, feel free to reach out to this mail.\n\nThanks!\n Team Techies"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
def send_register_volunteer(user_email,username,event):
    subject='Volunteer Registration'
    message=f'Hi {username},\n You are succesfully registered as Volunteer {event}'
    from_email=settings.DEFAULT_FROM_EMAIL
    recipient_list=[user_email]

    send_mail(subject,message,from_email,recipient_list)

def send_unregister_volunteer(user_email,username,event):
    subject='Voluntree unregistration'
    message=f'Hi {username},\n You are succesfully unregistered as Volunteer {event}'
    from_email=settings.DEFAULT_FROM_EMAIL
    recipient_list=[user_email]

    send_mail(subject,message,from_email,recipient_list)