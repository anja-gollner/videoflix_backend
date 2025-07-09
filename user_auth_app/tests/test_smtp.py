import smtplib
import ssl
import certifi

context = ssl.create_default_context(cafile=certifi.where())
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls(context=context)
    server.login("anjakgollner@gmail.com", "vlfe vzct mukt khzu")
    print("Verbindung erfolgreich!")
    server.quit()
except Exception as e:
    print(f"Fehler: {e}")