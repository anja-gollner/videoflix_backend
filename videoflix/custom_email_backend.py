import certifi
import ssl
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
import smtplib

class CustomEmailBackend(SMTPBackend):
    def open(self):
        # Prüfe, ob bereits eine Verbindung besteht
        if self.connection:
            return False
        try:
            # Erstelle die SMTP-Verbindung manuell
            self.connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
            
            # Aktiviere TLS, falls erforderlich
            if self.use_tls:
                context = ssl.create_default_context(cafile=certifi.where())
                self.connection.starttls(context=context)
            
            # Melde dich an, falls Benutzername und Passwort vorhanden sind
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            
            return True
        except Exception:
            if not self.fail_silently:
                raise