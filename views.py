from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from config import UPLOAD_PATH
from main import app, db
from models import Documentos, Grupos, Professores

@app.route('/')
def index():
    session['orientador_logado'] = None
    return render_template('tipo_login.html', titulo='Escolher login')

@app.route('/login/professor')
def login_professor():
    return render_template('login_professor.html', titulo='Login Professor')

@app.route('/login/grupo')
def login_grupo():
    return render_template('login_grupo.html', titulo='Login Grupo')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    professor = Professores.query.filter_by(email=request.form['usuario']).first()
    grupo = Grupos.query.filter_by(email=request.form['usuario']).first()
    if(professor):
        if(request.form['senha'] == professor.senha):
            session['usuario_logado'] = professor.id_professor
            session['permissao'] = professor.permissao
            session['orientador_logado'] = professor.id_professor
            session['grupo_logado'] = 'não'
            if(session['permissao']):
                return redirect(url_for('orientadores'))
            return redirect(url_for('inicio'))
        else:
            flash("Usuário ou senha incorretos.")
            return redirect(url_for('login'))
    elif(grupo):
        if(request.form['senha'] == grupo.senha):
            session['usuario_logado'] = grupo.nome
            session['orientador_logado'] = None
            session['grupo_logado'] = 'sim'
            return redirect(url_for('inicio'))
        else:
            flash("Usuário ou senha incorretos.")
            return redirect(url_for('login_grupo'))  
    else:
        flash("Usuário ou senha incorretos.")
        return redirect(url_for("index"))


@app.route('/inicio')
def inicio():
    if(session['usuario_logado'] == None):
        return redirect(url_for('login'))
    if(session['orientador_logado'] != None):
        grupos = Grupos.query.filter_by(orientador=int(session['usuario_logado']))
    else:
        grupos = Grupos.query.filter_by(nome=str(session['usuario_logado']))
    documentos = Documentos.query.filter_by()
    return render_template('inicio.html', titulo='Início', grupos=grupos, documentos=documentos, permissao=session['permissao'], grupo_logado=session['grupo_logado'])

@app.route('/pegar_arquivo/<nome_do_arquivo>', methods=['GET',])
def get_arquivo(nome_do_arquivo):
    if(session['usuario_logado'] == None):
        return redirect(url_for('login'))
    return send_from_directory(UPLOAD_PATH, nome_do_arquivo)

@app.route('/arquivos', methods=['POST', ])
def post_arquivo():
    arquivo = request.files['arquivo']
    print(arquivo.content_type)
    grupo = request.form['grupo']
    id_documento = int(request.form['id_documento'])
    nome_arquivo = f'{grupo}-{arquivo.filename}'
    url = f'{UPLOAD_PATH}/{grupo}-{arquivo.filename}'
    arquivo.save(url)
    documento = Documentos.query.filter_by(id_documento=id_documento).first()
    documento.arquivo = nome_arquivo
    db.session.add(documento)
    db.session.commit()    
    return redirect(url_for('inicio'))

@app.route('/deletar_arquivo/<int:id_documento>')
def excluir_arquivo(id_documento):
    if(session['usuario_logado'] == None):
        return redirect(url_for('login'))
    documento = Documentos.query.filter_by(id_documento=id_documento).first()
    documento.arquivo = None
    db.session.add(documento)
    db.session.commit()
    return redirect(url_for('inicio'))

@app.route('/grupos')
def grupos():
    if(session['usuario_logado'] == None):
        return redirect(url_for('login'))
    grupos = Grupos.query.filter_by(orientador=int(session['usuario_logado']))
    return render_template('grupos.html', titulo='Grupos', grupos=grupos, orientador=session['usuario_logado'])

@app.route('/cadastrar_grupo', methods=['POST', ])
def cadastrar_grupo():
    if(session['usuario_logado'] == None):
        return redirect(url_for('login'))
    gru = Grupos.query.filter_by(nome=request.form['nome']).first()
    if(gru):
        flash('Nome de grupo já cadastrado. Escolha outro nome.', category='warning')
        return redirect(url_for('grupos'))
    else:    
        grupo = Grupos(nome=request.form['nome'], email=request.form['email'], senha=request.form['senha'], orientador=int(request.form['id_professor']), turma=request.form['turma'])
        db.session.add(grupo)
        db.session.commit()
        flash("Grupo {} cadastrado com sucesso!".format(request.form['nome']), category='success')
        return redirect(url_for('grupos'))


@app.route('/excluir_grupo/<nome>')
def excluir_grupo(nome):
    if(session['usuario_logado'] == None):
        return redirect(url_for('login'))
    Grupos.query.filter_by(nome=nome).delete()
    db.session.commit()
    return redirect(url_for('grupos'))

@app.route('/orientadores')
def orientadores():
    if(session['usuario_logado'] == None):
        return redirect(url_for('login'))
    if(session['permissao'] == None):
        flash("Acesso só para coordenadores.", category='warning')
        return redirect(url_for('login'))
    
    return render_template('orientadores.html', titulo='Orientadores')

@app.route('/entregas')
def entregas():
    if(session['usuario_logado'] == None):
        return redirect(url_for('login'))
    grupos = Grupos.query.filter_by(orientador=int(session['usuario_logado']))
    documentos = Documentos.query.all()
    return render_template('entregas.html', titulo='Atribuir Entregas', grupos=grupos, documentos=documentos)

@app.route('/cadastrar_entregas', methods=['POST', ])
def cadastrar_entregas():
    if(session['usuario_logado'] == None):
        return redirect(url_for('login'))
    grupo = Grupos.query.filter_by(nome=request.form['grupo']).first()
    documento = Documentos(nome=request.form['nome'], turma=grupo.turma, grupo=request.form['grupo'], data_hora=request.form['prazo'], avaliacao='PENDENTE')
    
    db.session.add(documento)
    db.session.commit()
    
    return redirect(url_for('entregas')) 

@app.route('/excluir_entrega', methods=['GET'])
def excluir_entrega():
    if(session['usuario_logado'] == None):
        return redirect(url_for('login'))
    Documentos.query.filter_by(id_documento=int(request.args['id_documento'])).delete()
    db.session.commit()
    return redirect(url_for('entregas'))

@app.route('/atribuir_nota', methods=['POST', ])
def atribuir_nota():
    id_documento = request.form['id_documento']
    avaliacao = request.form['avaliacao']
    print(id_documento)
    print(avaliacao)
    documento = Documentos.query.filter_by(id_documento=id_documento).first()
    documento.avaliacao = avaliacao
    db.session.add(documento)
    db.session.commit()
    return redirect(url_for('inicio'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    session['permissao'] = None
    session['orientador_logado'] = None
    session['grupo_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))
