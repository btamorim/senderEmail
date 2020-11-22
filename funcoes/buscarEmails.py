import cx_Oracle
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
dns=config.get('BD', "dns")
user=config.get('BD', "user")
pwd=config.get('BD', "pwd")
db_pool = cx_Oracle.SessionPool(user, pwd, dns, min = 1, max = 3, increment = 1, threaded = True, encoding="UTF-8",nencoding='UTF-8')

def buscaEmailSender(nrlote):
    connection = db_pool.acquire()
    cursor = connection.cursor()
    query = "select ped_str_ds_email email, ped_str_ds_nome1||' '||ped_str_ds_nome2 nome, l.loc_str_ds_nomeorgao local \
                from cartao_idt.spif_pedidocarteira pd \
                inner join cartao_idt.spif_localentrega l on (l.loc_int_id_local = pd.loc_int_id_local) \
                where pd.lot_int_id_lote = :nr_lote" 
    try:
        cursor.execute(query,{'nr_lote': nrlote})
        result=cursor.fetchall()
        if not result:
            print(result)
            return ('nenhum pedido encontrado',404)

        saida = [dict(zip([key[0] for key in cursor.description], row)) for row in result]
        return saida
   
    except Exception as e:
        print('erro ao buscar, campo: {}'.format(e))
    finally:
        cursor.close()
        db_pool.release(connection)