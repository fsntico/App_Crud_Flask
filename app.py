from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    telefone = db.Column(db.String(15))
    senha = db.Column(db.String(80), nullable=False)
    empresa = db.Column(db.String(120), nullable=False)

@app.route('/')
def index():
    pessoas = Pessoa.query.all()
    return render_template('index.html', pessoas=pessoas)
@app.route('/cadastroproduto')
def cadastro_produto():
    return render_template('cadastro_produto.html')
@app.route('/adicionar', methods=['POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']
        senha2 = request.form['senha2']
        empresa = request.form['empresa']

        if senha != senha2:
            flash('As senhas não coincidem!', 'error')
        else:
            pessoa = Pessoa(nome=nome, email=email, telefone=telefone, senha=senha, empresa=empresa)
            db.session.add(pessoa)
            db.session.commit()
            flash('Pessoa adicionada com sucesso!', 'success')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    pessoa = Pessoa.query.get(id)
    db.session.delete(pessoa)
    db.session.commit()
    flash('Pessoa removida com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)