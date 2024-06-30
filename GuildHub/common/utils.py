from django.core.mail import EmailMultiAlternatives


def send_email(subject, text_content, html_content, recipient_list, from_email=None):
    """
    Send an email.
    """
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
