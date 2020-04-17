from flask import Flask, Blueprint, abort
from flask_restplus import Resource, Api

import configparser
from funcoes import *

config = configparser.ConfigParser()
config.read("config.ini")

pwd=config.get("CONF", "password")
port=config.get("CONF", "port")
sender_mail=config.get("CONF", "sender_email")
server_smtp=config.get("CONF", "server_smtp")
assunto=config.get("MSG", "Subject") 

app = Flask(__name__)
blueprint = Blueprint('api', __name__)
api = Api(blueprint, 
            doc='/doc' ,
            version='v1',
            title='API APOIO A IDENTIFICACAO', description='Envio de Email aos vinculados que soliucitaram a CIM',
            default="EMAIL",
            default_label="Notificação por EMAIL"
            )

app.config['JSON_AS_ASCII'] = False
app.register_blueprint(blueprint)

@api.route('/enviaMail/<nrlote>')
@api.param('nrlote', 'numero do lote')
@api.doc( description="Função que busca no banco os dados do lote para enviar os emails de notificação")
class mail(Resource):

    def get(self, nrlote):
        dadosEnvio = fn_buscaEmailSender(nrlote)
        for dados in dadosEnvio:
            print(dados['EMAIL'])
            print(dados['NOME'])
            print(dados['LOCAL'])
            #envio = fn_enviar(server_smtp, port, sender_mail, pwd, mail, assunto, nome, local )
            return 200

#print(fn_buscaEmailSender(60495))
#mail="amorim.bruno@eb.mil.br"
#envio = fn_enviar(server_smtp, port, sender_mail, pwd, mail, assunto )

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    #app.run( debug=True)
