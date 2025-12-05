from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_html_email(subject, template_name, context, recipient_list, from_email=None):
    if not recipient_list:
        return
    html_message = render_to_string(template_name, context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=html_message,
        from_email=from_email,
        to=recipient_list
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)
