from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from os import getenv
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(20), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    categoria_perda = db.Column(db.String(100), nullable=False)
    pix = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"User('{self.nome}', '{self.cpf}', '{self.telefone}')"


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        email = request.form['email']
        endereco = request.form['endereco']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        descricao = request.form['descricao']
        categoria_perda = request.form['categoria_perda']
        pix = request.form['pix']
        senha = request.form['senha']

        # Criptografar a senha antes de salvar
        senha_hash = generate_password_hash(senha)

        new_user = User(nome=nome, cpf=cpf, telefone=telefone, email=email,
                        endereco=endereco, bairro=bairro, cidade=cidade,
                        descricao=descricao, categoria_perda=categoria_perda,
                        pix=pix, senha=senha_hash)

        db.session.add(new_user)
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            return str(e)  # Para propósitos de debugging, mostrar a exceção

    return render_template('register.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, senha):
            login_user(user)
            return redirect(url_for('update'))
        else:
            flash('Login failed. Check your credentials.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        current_user.nome = request.form['nome']
        current_user.email = request.form['email']
        # update other fields
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('update'))
    return render_template('update.html', user=current_user)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
