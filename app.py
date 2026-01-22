from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ded1fd07da2fa3688dd5b5a6338153912b97b8ed735a35b8439776a8075893d1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bar_database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- MODELOS DO BANCO DE DADOS ---

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artista = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    horario = db.Column(db.String(10), nullable=False)
    imagem = db.Column(db.String(200))

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False) # Bebida, Drink ou Comida
    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(200))

class Galeria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    arquivo = db.Column(db.String(200), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROTAS DO SITE ---

@app.route('/')
def index():
    shows = Show.query.all()
    produtos = Produto.query.all()
    fotos = Galeria.query.all()
    return render_template('index.html', shows=shows, produtos=produtos, fotos=fotos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Aqui depois faremos a lógica de login
    return render_template('login.html')

# Rota secreta para o login do dono
@app.route('/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('admin.html') # Você precisa ter este arquivo HTML!

@app.route('/excluir-produto/<int:id>')
@login_required # Garante que só o admin logado consiga deletar
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar-produto/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        produto.nome = request.form.get('nome')
        produto.preco = request.form.get('preco')
        produto.categoria = request.form.get('categoria')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', produto=produto)

@app.route('/adicionar-produto', methods=['GET', 'POST'])
@login_required
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        categoria = request.form.get('categoria')
        descricao = request.form.get('descricao')
        
        novo_item = Produto(nome=nome, preco=float(preco), 
                            categoria=categoria, descricao=descricao)
        
        db.session.add(novo_item)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('adicionar.html')

@app.route('/adicionar-show', methods=['GET', 'POST'])
@login_required
def adicionar_show():
    if request.method == 'POST':
        artista = request.form.get('artista')
        data = request.form.get('data')
        horario = request.form.get('horario')
        
        novo_show = Show(artista=artista, data=data, horario=horario)
        db.session.add(novo_show)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('adicionar_show.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# --- INICIALIZAÇÃO ---

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Cria o arquivo .db e as tabelas
    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)
