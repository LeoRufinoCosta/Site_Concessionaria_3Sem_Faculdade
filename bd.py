UP_FOLDER = 'C:\\Users\\leonardo.fc\\Desktop\\TRABALHOPRAHJ-master\\imagens\\carros'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def config(app):
    app.config['UP_FOLDER'] = UP_FOLDER
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
    app.config['MYSQL_DATABASE_DB'] = 'concessionaria'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db(mysql):
    conn = mysql.connect()
    cursor = conn.cursor()

    return conn, cursor

def get_idlogin(cursor, login, senha):
    cursor.execute(f'SELECT idlogin FROM login WHERE login = "{login}" and senha = "{senha}"')
    idlogin = cursor.fetchone()
    cursor.close()
    return idlogin

def get_carros(cursor):
    cursor.execute(f'SELECT idcarros, nome, marca, quilometragem, combustivel, cor, cambio, ano, preco, top10, imagem FROM carros')
    carros = cursor.fetchall()
    return carros

def del_car(cursor, conn, idcarros):
    cursor.execute(f'DELETE FROM carros WHERE idcarros = {idcarros}')
    conn.commit()

def consultar_carros(cursor, buscando):
    cursor.execute(f'SELECT idcarros, nome, marca, quilometragem, combustivel, cor, cambio, ano, preco, imagem FROM carros WHERE nome = "{buscando}"')
    consulta = cursor.fetchall()
    cursor.close()
    return consulta

def add_user(cursor, conn, login, senha):
    cursor.execute(f'INSERT INTO login (login, senha) values("{login}", "{senha}")')
    conn.commit()

def del_user(cursor, conn, idlogin):
    cursor.execute(f'DELETE FROM login WHERE idlogin = {idlogin}')
    conn.commit()

def listar_login(cursor):
    cursor.execute(f'SELECT idlogin, login, senha FROM login')
    logins=cursor.fetchall()
    return logins

def inserir_anun(cursor, conn, nome, marca, quilometragem, combustivel, cor, cambio, ano, preco, top10, imagem):
    cursor.execute(f'INSERT INTO carros (nome, marca, quilometragem, combustivel, cor, cambio, ano, preco, top10, imagem) values("{nome}", "{marca}", "{quilometragem}", "{combustivel}", "{cor}", "{cambio}", "{ano}", "R${preco},00", "{top10}", "{imagem}")')
    conn.commit()

def reservar(cursor, conn, idcarros):
    cursor.execute(f'INSERT INTO reservas (idcarros, nome, marca, quilometragem, combustivel, cor, cambio, ano, preco, imagem) SELECT idcarros, nome, marca, quilometragem, combustivel, cor, cambio, ano, preco, imagem from carros WHERE idcarros = {idcarros}')
    cursor.execute(f'DELETE FROM carros WHERE idcarros = {idcarros}')
    conn.commit()

def listar_reserva(cursor):
    cursor.execute(f'SELECT idreservas, nome, marca, quilometragem, combustivel, cor, cambio, ano, preco, imagem, nomepessoa, email, telefone FROM reservas')
    reserva=cursor.fetchall()
    return reserva

def desreservar(cursor, conn, idcarros):
    cursor.execute(f'INSERT INTO carros (nome, marca, quilometragem, combustivel, cor, cambio, ano, preco, imagem) SELECT nome, marca, quilometragem, combustivel, cor, cambio, ano, preco, imagem FROM reservas WHERE idreservas = {idcarros}')
    cursor.execute(f'DELETE FROM reservas WHERE idreservas = {idcarros}')
    conn.commit()

def finalizar_reserva(cursor, conn, nome, email, telefone, idcarros):
    cursor.execute(f'UPDATE reservas SET nomepessoa="{nome}", email="{email}", telefone="{telefone}" WHERE idcarros={idcarros}')
    conn.commit()

def get_idcarros(cursor, idcarros):
    cursor.execute(f'SELECT idcarros, nomepessoa, email, telefone FROM reservas WHERE idcarros = {idcarros} ')
    carros = cursor.fetchone()
    return carros

def reclame_aqui(cursor,conn, nome, telefone, email, reclamacao):
    cursor.execute(f'INSERT INTO reclamacao(nome, telefone, email, reclamacao) values("{nome}","{telefone}", "{email}", "{reclamacao}")')
    conn.commit()

def listar_reclama(cursor):
    cursor.execute(f'SELECT idreclamacao, nome, telefone, email, reclamacao from reclamacao')
    reclamacoes = cursor.fetchall()
    return reclamacoes

def del_reclamacao(cursor, conn, idreclamcao):
    cursor.execute(f'DELETE FROM reclamacao WHERE idreclamacao = {idreclamcao}')
    conn.commit()

def view_listavip(cursor):
    top='sim'
    cursor.execute(f'SELECT idcarros, nome, marca, quilometragem, combustivel, cor, cambio, ano, preco, imagem FROM carros WHERE top10 ="{top}"')
    top10 = cursor.fetchall()
    return top10

def view_no_listavip(cursor):
    top='não'
    cursor.execute(f'SELECT idcarros, nome, marca, quilometragem, combustivel, cor, cambio, ano, preco, imagem FROM carros WHERE top10 ="{top}"')
    carru = cursor.fetchall()
    return carru

def put_top10(cursor, conn, idcarros):
    cursor.execute(f'UPDATE carros SET top10="Sim" WHERE idcarros= {idcarros}')
    conn.commit()

def remove_top10(cursor, conn, idcarros):
    cursor.execute(f'UPDATE carros SET top10="Não" WHERE idcarros= {idcarros}')
    conn.commit()

def detalhes(cursor, idcarros):
    cursor.execute(f'SELECT idcarros, nome, marca, quilometragem, combustivel, cor, cambio, ano, preco, imagem FROM carros WHERE idcarros = {idcarros}')
    detalhe = cursor.fetchall()
    return detalhe