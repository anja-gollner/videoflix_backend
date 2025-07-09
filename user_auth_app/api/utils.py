import certifi
import ssl
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def send_activation_email(user, activation_link, email, mail_subject="Confirm your email"):
    # Render die E-Mail-Vorlage
    message = render_to_string("user_auth_app/email_verification.html", {
        "user": user,
        "activation_link": activation_link
    })

    # Erstelle die E-Mail-Nachricht
    email_message = EmailMessage(
        subject=mail_subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    email_message.content_subtype = "html"  # Setze den Inhaltstyp auf HTML

    # Sende die E-Mail direkt (der Backend übernimmt die Verbindung)
    email_message.send(fail_silently=False)