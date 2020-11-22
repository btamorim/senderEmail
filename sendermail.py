from flask import Flask, Blueprint, abort, request
from flask_restx import Resource, Api, fields
import json
import ssl
import configparser
from funcoes import *

from validate_email import *

config = configparser.ConfigParser()
config.read("config.ini")


pwd=config.get("CONF", "password", fallback="")
port=config.get("CONF", "port")
sender_mail=config.get("CONF", "sender_email")
server_smtp=config.get("CONF", "server_smtp")
smtp_use_ssl=config.getboolean("CONF", "smtp_use_ssl", fallback=True)
assunto=config.get("MSG", "Subject") 
proxy=config.get("CONF", "proxy_addr")


app = Flask(__name__)
blueprint = Blueprint('api', __name__)
api = Api(blueprint, 
            doc='/doc' ,
            version='v1',
            title='API DE ENVIO DE EMAIL', description='Envio de Email aos vinculados do sistema.',
            default="EMAIL",
            default_label="Notificação por EMAIL"
            )

app.config['JSON_AS_ASCII'] = False
app.register_blueprint(blueprint)

email_ind = api.model('mail', {
    'email': fields.String(required=True, description='Email a ser enviado'),
    'assunto': fields.String(required=True, description='Assunto do Email'),
    'mensagem': fields.String(required=True, description='Mensagem do Email')
    })


@api.route('/enviaMailLote/<nrlote>')
@api.param('nrlote', 'numero do lote')
@api.doc( description="Função que busca no banco os dados do lote para enviar os emails de notificação")
class mailLote(Resource):

    def get(self, nrlote):
        dadosEnvio = fn_buscaEmailSender(nrlote)
        envio = None
        for dados in dadosEnvio:
            print(dados)
            fila = fz_insereMailFila(2, dados['EMAIL'], assunto, None, dados['NOME'], dados['LOCAL'])
            #envio = fn_enviar_lote(server_smtp, port, sender_mail, pwd, dados['EMAIL'], assunto, dados['NOME'], dados['LOCAL'], smtp_use_ssl)
        
        return fila

@api.route('/enviaMail')

@api.doc( description="Função que enviar os emails de notificação")
class mailIndividual(Resource):
    @api.doc(body=email_ind)
    def post(self):
        erro = None
        is_valid = True
        data = json.loads(request.data)

        if(is_valid == True):
            
            print("chamando o fz_insereMailFila")
            fila = fz_insereMailFila(1,data['email'], data['assunto'], data['mensagem'])
            return fila
        else:
            return {"mensagem": "erro ao enviar. Error:{}".format(erro)},409

from verifier.verifier import Verifier 
@api.route('/validarMail/<email>')
@api.param('email', 'O email a ser validado')
@api.doc( description="Função que valida se o email existe e tem o formato correto")
class validarEmail(Resource):

    def post(self, email):
        erro = None
        try:
            #função verifier a estrutura e o servidor SMTP (GMAIL, YAHOO, ETC)
            sockes_verifier = Verifier(
                source_addr= sender_mail
                )
            results = sockes_verifier.verify(email)
            return results
            
        except Exception as e:
            ##check_regex checa a estrutura do email esta correta
            ##check_mx: checa se o email existe
            #função da lib validate_email
            is_valid = validate_email(email,
                check_mx= True, smtp_timeout=10, debug=True)
            print('is_valid:{}'.format(is_valid))
            print("no exception validate email")
            print('o erro foi: {}'.format(e))
            return is_valid, 400        

@api.route('/mailNaoEnviado')
@api.doc( description="Função que busca os emails que tiveram problemas para serem enviados. ")
class mailNaoEnviado(Resource):

    def get(self):
        try:
            fz_criaDB()
            emails = fz_buscaMailNaoEnviado()
            print(emails)
            return emails
        except Exception as e:
            print("exceptio,:{}".format(e))


@api.route('/enviaEmailAnexo/<email>/<assunto>/<mensagem>')
@api.param('email', 'O email a ser validado')
@api.param('assunto', 'O assunto do email')
@api.param('mensagem', 'A msg a ser enviada')
@api.doc( description="Função que envia email no template padrão")
class enviarMailIndTemp(Resource):

    def get(self, email, assunto, mensagem):
        try:

            emails = fz_enviarMailIndTemp(1, server_smtp, port, sender_mail, pwd, email, assunto, mensagem, smtp_use_ssl)
            print(emails)
            return emails
        except Exception as e:
            print("exceptio,:{}".format(e))


if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    app.run(host='0.0.0.0', debug=True)

