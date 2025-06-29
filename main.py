from flask import Flask, render_template, request, session, url_for, redirect
import gestaoDB

gestaoDB.criarTabelaUsuario()

app = Flask (__name__)
app.secret_key = 'alguma_chave_secreta_segura'

#rota principal onde estara todo o conteudo da pagina sendo possivel reconecher todas as rotas detinadas do software
@app.route('/')
def paginaHome():
    return render_template('home.html')

@app.route('/cadastrar')
def paginaCriarConta():
    return render_template('cadastrar.html')

#rota para receber os dados do usuário e cadastrar novo usuário na lista
@app.route("/cadastrarUsuario", methods=['POST'])
def cadastrarUsuario():
    nome = request.form.get('nomeUsuario')
    conta = request.form.get('contaUsuario')
    email = request.form.get('emailUsuario')
    senha = str(request.form.get('senhaUsuario'))
    if(gestaoDB.verificarUsuario(email)==False):
        gestaoDB.inserirUsuario(nome, conta, email, senha)
        mensagem="usuário cadastrado com sucesso"
        return render_template("home.html", mensagem=mensagem)
    else:
        mensagem="usuário já existe"
        return render_template("home.html", mensagem)
    
#rota para receber login e senha e fazer a autenticação (login)
@app.route("/autenticarUsuario", methods=['POST'])
def autenticar():
    email = request.form.get("emailUsuario")
    senha = str(request.form.get("senhaUsuario"))
    
    logado=gestaoDB.login(email, senha)

    if(logado==True):
        return render_template("logado.html")
    else:    
        mensagem="usuario ou senha incorreto"
        return render_template("home.html", mensagem=mensagem)

@app.route('/recuperarConta')
def paginaRecuperarConta():
    return render_template('recuperarConta.html')

@app.route("/form-recuperar", methods=['POST'])
def recuperarSenha():
    conta = request.form.get("contaUsuario")
    email = request.form.get("emailUsuario")
   
    encontrado=False
    senha="vazio"

    if(gestaoDB.verificarUsuario(email)==True):
        encontrado=True

    if(encontrado==True):
        senha = str(gestaoDB.recuperarSenhaBD(conta, email))
        mensagem="sua senha"+senha
        return render_template("recuperarConta.html", mensagem=mensagem)
    else:    
        mensagem="usuario nao encontrado"
        return render_template("recuperarConta.html", mensagem=mensagem)
    

@app.route("/logout")
def logout():
    usuario = gestaoDB.listarUsuarios() 
    session.pop('usuario', None)
    usuarios = gestaoDB.listarUsuarios()  
    return redirect(url_for('paginaHome', usuario=usuario)) 
    
@app.route('/downloadGamer')
def paginaDownload():
    return render_template('downloadGamer.html')

@app.route('/tutorial')
def paginaTutorial():
    return render_template('tutorial.html')

@app.route('/usuario')
def paginaUsuario():
    usuarios = gestaoDB.listarUsuarios()  
    return render_template('usuario.html', usuarios=usuarios)


@app.route('/ranking')
def paginaRaking():
    return render_template('ranking.html')

@app.route('/regras')
def paginaRegras():
    return render_template('regras.html')

@app.route('/mapaJogo')
def paginaMapaJogo():
    return render_template('mapaJogo.html')

@app.route('/video')
def paginaVideo():
    return render_template('video.html') 

@app.route('/forum')
def paginaForum():
    return render_template('forum.html')

@app.route('/treinadorOnline')
def paginaTreinadorOnline():
    return render_template('treinadorOnline.html')          

if __name__ == '__main__':
    app.run(debug=True)