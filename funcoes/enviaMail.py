from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from email.header import Header
import email.mime.application

from email.mime.base import MIMEBase
from email import encoders
import os.path

def enviarMail(server_smtp, port, sender_mail, pwd, mail,  assunto, nome, local, use_ssl=True ):
    message = MIMEMultipart()
    message['Content-Type'] = 'text/html; charset=utf-8'
    message["From"] = sender_mail
    message["To"] = mail
    message["Subject"] = Header(assunto, 'utf-8')
    message["Bcc"] = None
    dicionario = {}
    dicionario['nome'] = nome
    dicionario['local'] = local

    with open('template.html', encoding="utf-8") as template_file:
        html = template_file.read().format(**dicionario)

    part = MIMEText(html, 'html', 'utf-8')
    message.attach(part)
    try:
        print("dentroEnvia mail")
        if use_ssl:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(server_smtp, port, context=context) as server:
                server.login(sender_mail, pwd)
                server.sendmail(sender_mail, mail,  message.as_string())
        else:
            with smtplib.SMTP(server_smtp, port) as server:
                server.sendmail(sender_mail, mail,  message.as_string())
        return 200
    except Exception as e:
        print("mensagem Não foi possivel enviar o email. Erro:{}".format(e))
        return 409
    

def enviarMailIndividual(server_smtp, port, sender_mail, pwd, mail, assunto, mensagem, use_ssl=True ):
    message = MIMEMultipart()
    message['Content-Type'] = 'text/html; charset=utf-8'
    message["From"] = sender_mail
    message["To"] = mail
    message["Subject"] = Header(assunto, 'utf-8')
    message["Bcc"] = None

    part = MIMEText(mensagem, 'html', 'utf-8')
    message.attach(part)

    try:

        print("dentroEnvia mail")
        if use_ssl:
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(server_smtp, port, context=context) as server:
                server.login(sender_mail, pwd)
                server.sendmail(sender_mail, mail,  message.as_string())
        else:
            with smtplib.SMTP(server_smtp, port) as server:
                server.sendmail(sender_mail, mail,  message.as_string())
        print("dentroEnvia depois envio")
        return 200

    except Exception as e:
        print(e)
        return 409
    
from io import BytesIO
def enviarMailIndTemp(tipo, server_smtp, port, sender_mail, pwd, mail, assunto, mensagem, use_ssl=True ):
    message = MIMEMultipart()
    #message['Content-Type'] = 'application/pdf; charset=UTF-8'
    message["From"] = sender_mail
    message["To"] = mail
    message["Subject"] = Header(assunto, 'utf-8')
    message["Bcc"] = None

    part = MIMEText(mensagem, 'html', 'utf-8')
    #message.attach(part)
    message.attach(MIMEText(message, 'plain'))


    filename = os.path.basename('arquivo.txt')

    try:
        temp = open(filename, 'rb')
        attachement = MIMEApplication(temp.read(), _subtype='pdf')
        temp.close()
        encoders.encode_base64(attachement)  #https://docs.python.org/3/library/email-examples.html
        attachement.add_header('Content-Disposition', 'attachment', filename=filename) # name preview in email
        message.attach(attachement) 
    except Exception as e:
        print(e)


    try:

        print("dentroEnvia mail")
        if use_ssl:
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(server_smtp, port, context=context) as server:
                server.login(sender_mail, pwd)
                server.sendmail(sender_mail, mail,  message.as_string())
        else:
            with smtplib.SMTP(server_smtp, port) as server:
                server.sendmail(sender_mail, mail,  message.as_string())
        print("dentroEnvia depois envio")
        return 200

    except Exception as e:
        print(e)
        return 409
