#gerenciaMailEnvio.py
import sqlite3
import queue
import threading
from funcoes import *
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

pwd=config.get("CONF", "password", fallback="")
port=config.get("CONF", "port")
sender_mail=config.get("CONF", "sender_email")
server_smtp=config.get("CONF", "server_smtp")
smtp_use_ssl=config.getboolean("CONF", "smtp_use_ssl", fallback=True)
assunto=config.get("MSG", "Subject") 
proxy=config.get("CONF", "proxy_addr") 

import time

def enviarMail(q, email, assunto, mensagem):
	while not q.empty():
		time.sleep(10)
		envio = fn_enviar_individual(server_smtp, port, sender_mail, pwd, email, assunto, mensagem, smtp_use_ssl)

		if(envio == 200):
			q.get()
		else:
			q.get()
			insereMailNaoEnviado(email, assunto, mensagem)

def enviarMailLote(q, email, assunto, nome, local):
	while not q.empty():
		time.sleep(10)
		envio = fn_enviar_lote(server_smtp, port, sender_mail, pwd, email, assunto, nome, local, smtp_use_ssl)

		if(envio == 200):
			q.get()
		else:
			q.get()
			insereMailNaoEnviado(email, assunto, "lote recebido")

def insereMailFila(tipo, email, assunto, mensagem, nome = None, local= None):
	#tipo 1 ->individual - tipo 2 ->lote
	try:
		q = queue.Queue()
		q.put(email)
		if(tipo == 1):
			t = threading.Thread(target = enviarMail, args = (q, email, assunto, mensagem), daemon =True)
		else:
			t = threading.Thread(target = enviarMailLote, args = (q, email, assunto, nome, local), daemon =True)

		t.start()

		return {"mensagem":"e-mail na fila de envio"},200
	except Exception as e:
		print(e)

def insereMailNaoEnviado(email, assunto, mensagem):
	try:
		criaDB()
		conn = sqlite3.connect('mail.db')
		conn.cursor()
		dados = (email,assunto,mensagem)
		conn.execute('INSERT INTO ENVIO_EMAIL (email, assunto, mensagem) VALUES (?, ?, ?)', dados)
		conn.commit()
		
	except Exception as e:
		print(e)
		return 400
	finally:
		conn.close()

def buscaMailNaoEnviado():
	try:
		
		conn = sqlite3.connect('mails.db')
		c = conn.cursor()
		c.execute('SELECT EMAIL, data FROM ENVIO_EMAIL')
		return c.fetchall()
		
	except Exception as e:
		print("O ERRO E:{}".format(e))
		return 400
	finally:
		conn.close()

def criaDB():
	try:

		conn = sqlite3.connect('mails.db')
		conn.cursor()
		conn.execute('''CREATE TABLE ENVIO_EMAIL (email text, assunto text, mensagem text, data datetime DEFAULT current_timestamp)''')
		conn.commit()
		return 200
	except Exception as e:
		print(e)
	finally:
		conn.close()