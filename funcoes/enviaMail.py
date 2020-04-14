from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from email.header import Header

def enviarMail(server_smtp, port, sender_mail, pwd, mail,  assunto ):
    message = MIMEMultipart()
    message['Content-Type'] = 'text/html; charset=utf-8'
    message["From"] = sender_mail
    message["To"] = mail
    message["Subject"] = Header(assunto, 'utf-8')
    message["Bcc"] = None
    dicionario = {}
    dicionario['nome'] = 'Bruno Amorim'
    dicionario['local'] = 'GIR 11'

    with open('template.html', encoding="utf-8") as template_file:
        html = template_file.read().format(**dicionario)

    part = MIMEText(html, 'html', 'utf-8')
    message.attach(part)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(server_smtp, port, context=context) as server:
        server.login(sender_mail, pwd)
        server.sendmail(sender_mail, mail,  message.as_string())