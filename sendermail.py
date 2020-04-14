# -*- coding: utf-8 -*-
import configparser
from funcoes import *

config = configparser.ConfigParser()
config.read("config.ini")

pwd=config.get("CONF", "password")
port=config.get("CONF", "port")
sender_mail=config.get("CONF", "sender_email")
server_smtp=config.get("CONF", "server_smtp")
assunto=config.get("MSG", "Subject") 


mail="amorim.bruno@eb.mil.br"
envio = fn_enviar(server_smtp, port, sender_mail, pwd, mail, assunto )