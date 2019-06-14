import os
from flask import Flask, flash, render_template, request, redirect, url_for, send_file, send_from_directory
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
from bd import*

app = Flask(__name__)
mysql = MySQL()
mysql.init_app(app)

config(app)

@app.route('/')
def home():
    cursor = mysql.get_db().cursor()
    x=view_listavip(cursor)
    print(x)
    return render_template('home.html', carro=view_listavip(cursor), url='http://127.0.0.1:5000/upload/')

@app.route('/upload/<filename>', methods=['GET','POST'])
def uploads_file(filename):
    return send_from_directory(app.config['UP_FOLDER'], filename)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        senha = request.form.get('senha')
        cursor = mysql.get_db().cursor()
        idlogin = get_idlogin(cursor, login, senha)
        if idlogin is None:
            return redirect(url_for('home'))
        else:
            return render_template('comandos.html')

    else:
        return redirect(url_for('home'))

@app.route('/comando')
def voltar():
    return render_template('comandos.html')

@app.route('/consultacarros', methods=['GET', 'POST'])
def consultacarros():
    if request.method == 'POST':
        buscando = request.form.get('buscando')
        cursor = mysql.get_db().cursor()
        loco = consultar_carros(cursor, buscando)
        if loco is None:
            return redirect(url_for('home'))
        else:
            cursor = mysql.get_db().cursor()
            return render_template('detalhes.html', consulta=consultar_carros(cursor, buscando), url='http://127.0.0.1:5000/upload/')
    else:
        return redirect(url_for('home'))

@app.route('/pag_add_user')
def teste():
    return render_template('add_user.html')

@app.route('/add_user', methods=['POST'])
def adicionar_usuario():
    if request.method == 'POST':
        login = request.form.get('login')
        senha = request.form.get('senha')

        conn, cursor = get_db(mysql)

        add_user(cursor, conn, login, senha)

        cursor.close()
        conn.close()
        return render_template('add_user.html', top="Usuario adicionado com sucesso!")

    else:
        return redirect(url_for('add_user'))

@app.route('/pag_del_user')
def delete():
    conn, cursor = get_db(mysql)
    logins = listar_login(cursor)
    cursor.close()
    conn.close()
    return render_template('del_user.html', logins=logins)

@app.route('/del_user/<idlogin>')
def delete2(idlogin):
    conn, cursor = get_db(mysql)
    del_user(cursor, conn, idlogin)
    cursor.close()
    conn.close()
    #return render_template('home.html')
    return redirect(url_for('delete'))


@app.route('/pag_inserir_anuncio')
def inserir_anuncio():
    return render_template('inserir_anun.html')

@app.route('/inserir_anun', methods=['POST'])
def adicionar_anuncio():
    global filename
    if request.method == 'POST':
        nome = request.form.get('nome')
        marca = request.form.get('marca')
        quilometragem = request.form.get('quilometragem')
        combustivel = request.form.get('combustivel')
        cor = request.form.get('cor')
        cambio = request.form.get('cambio')
        ano = request.form.get('ano')
        preco = request.form.get('preco')
        top10 = request.form.get('top10')
        file = request.form.get('file')
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_location = os.path.join(app.config['UP_FOLDER'], filename)
            print(filename)
            print(file_location)
            print(file_location)
            escaped_file_location = file_location.replace('\\', '/')
            print(escaped_file_location)
            file.save(os.path.join(app.config['UP_FOLDER'], filename))

        conn = mysql.connect()
        cursor = conn.cursor()
        inserir_anun(cursor, conn, nome, marca, quilometragem, combustivel, cor, cambio, ano, preco, top10, filename)
        cursor.close()
        conn.close()
        return render_template('inserir_anun.html', bom="Anuncio inserido com sucesso!")

    else:
        return redirect(url_for('inserir_anuncio'))

@app.route('/pag_del_anuncio')
def delete_car():
    conn, cursor = get_db(mysql)
    carros = get_carros(cursor)
    cursor.close()
    conn.close()
    return render_template('viewcars.html', carros=carros, url='http://127.0.0.1:5000/upload/')

@app.route('/del_anuncio/<idcarros>')
def delete_car2(idcarros):
    conn, cursor = get_db(mysql)
    del_car(cursor, conn, idcarros)
    cursor.close()
    conn.close()
    return redirect(url_for('delete_car'))

@app.route('/pag_reservas')
def reservas():
    conn, cursor = get_db(mysql)
    reserva = listar_reserva(cursor)
    cursor.close()
    conn.close()
    return render_template('reservas.html', reserva=reserva, url='http://127.0.0.1:5000/upload/')

@app.route('/tirar_reservas/<idcarros>')
def reservas2(idcarros):
    conn, cursor = get_db(mysql)
    desreservar(cursor, conn, idcarros)
    cursor.close()
    conn.close()
    return redirect(url_for('reservas'))

@app.route('/fazer_reservas/<idcarros>')
def reservas3(idcarros):
    conn, cursor = get_db(mysql)
    reservar(cursor, conn, idcarros)
    carros = get_idcarros(cursor, idcarros)
    cursor.close()
    conn.close()
    return render_template('concluir_reserva.html', carros=carros)

@app.route('/salvar_alteracao', methods=['POST'])
def salvar_alteracao():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        idcarros = request.form.get('idcarros')
        conn, cursor = get_db(mysql)
        finalizar_reserva(cursor, conn, nome, email, telefone, idcarros)
        cursor.close()
        conn.close()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/contato')
def reclame():
    return render_template('contato.html')

@app.route('/reclame_aqui', methods=['POST'])
def reclameaqui():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        reclamacao = request.form.get('reclamacao')
        conn, cursor = get_db(mysql)
        reclame_aqui(cursor, conn, nome, telefone, email, reclamacao)
        cursor.close()
        conn.close()
        return render_template('contato.html', top="Reclamacao feita com sucesso! Esperar a resposta dos adms.")

    else:
        return redirect(url_for('reclame_aqui'))

@app.route('/pag_reclamacoes')
def pag_reclama():
    conn, cursor = get_db(mysql)
    reclamacoes = listar_reclama(cursor)
    cursor.close()
    conn.close()
    return render_template('reclamacao.html', reclamacoes=reclamacoes)

@app.route('/del_reclamacao/<idreclamacao>')
def delete_reclama(idreclamacao):
    conn, cursor = get_db(mysql)
    del_reclamacao(cursor, conn, idreclamacao)
    cursor.close()
    conn.close()
    return redirect(url_for('pag_reclama'))

@app.route('/lista_vip')
def listavip():
    return render_template('lista_vip.html')

@app.route('/edit_listavip')
def edit_listvip():
    conn, cursor = get_db(mysql)
    carru = view_no_listavip(cursor)
    top10 = view_listavip(cursor)
    cursor.close()
    conn.close()
    return render_template('lista_vip.html', top10=top10, carru=carru, url='http://127.0.0.1:5000/upload/')

@app.route('/put_listavip/<idcarros>')
def putlistvip(idcarros):
    conn, cursor = get_db(mysql)
    put_top10(cursor, conn, idcarros)
    cursor.close()
    conn.close()
    return redirect(url_for('edit_listvip'))

@app.route('/remove_listavip/<idcarros>')
def removelistvip(idcarros):
    conn, cursor = get_db(mysql)
    remove_top10(cursor, conn, idcarros)
    cursor.close()
    conn.close()
    return redirect(url_for('edit_listvip'))

@app.route('/detalhes/<idcarros>')
def detail(idcarros):
    conn, cursor = get_db(mysql)
    detalhe = detalhes(cursor, idcarros)
    cursor.close()
    conn.close()
    return render_template('detalhes.html', consulta=detalhe, url='http://127.0.0.1:5000/upload/')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
