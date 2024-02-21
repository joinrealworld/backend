from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template import Context
# from notification.consts import EMAIL_MESSAGES
from django.template.loader import get_template
from django.conf import settings


def send_mail_with_template(mail_content, txt_template_path, html_template_path, subject, from_email, to_emails):
    mail_content = mail_content
    try:
        with open(settings.ROOT_DIR + txt_template_path) as f:
            full_msg = f.read()
        message = EmailMultiAlternatives(subject=subject, body=full_msg, from_email=from_email, to=[to_emails])
        html_template = get_template(settings.ROOT_DIR +html_template_path).render(mail_content)
        message.attach_alternative(html_template, 'text/html')
        message.send()
    except Exception as e:
        print("23----",e)


def send_account_verification_mail(first_name, verification_link, to_emails, from_email=settings.EMAIL_HOST_USER):
    subject = "Verify your email to create your Join Real World Account"
    mail_content = {'first_name': first_name, "verification_link":verification_link}
    txt_template_path = "templates/verify_email.txt"
    html_template_path = "templates/verify_otp.html"
    send_mail_with_template(mail_content, txt_template_path, html_template_path, subject, from_email, to_emails)
