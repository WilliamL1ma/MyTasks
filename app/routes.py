from flask import render_template, request, redirect, flash, session, url_for
from app import app
from app.tasks_manager import add_task, view_tasks, remove_task, view_old_tasks
from app.auth import register_user, login_user
from app.decorators import login_required
from app.email.reset_password_bot import enviar_email_recuperacao
from pathlib import Path
import json
import bcrypt
from cryptography.fernet import Fernet

# Configuração da chave secreta para as sessões
app.secret_key = 'bomdia'

CAMINHO_USER = Path(__file__).parent / 'data' / 'users.json'

# Caminho para o arquivo da chave
key_file_path = Path(__file__).parent.parent / 'data' / 'secret.key'

# Inicializa o Fernet
fernet = None  # Inicializa fernet como None

try:
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()
        fernet = Fernet(key)  # Inicializa o Fernet com a chave
except FileNotFoundError:
    print(f"Arquivo não encontrado: {key_file_path}")
except Exception as e:
    print(f"Erro ao inicializar o Fernet: {e}")

@app.route('/')
def login():
    return render_template('login.html')  # Retorna a página de login

@app.route('/mytasks', methods=['GET'])
@login_required
def index():
    user_id = session.get('user_id')  # Pega o ID do usuário logado
    tasks = view_tasks(user_id)
    old_tasks = view_old_tasks(user_id)
    return render_template('index.html', tasks=tasks, old_tasks=old_tasks)

@app.route('/add_task', methods=['POST'])
@login_required
def add_task_route():
    title = request.form['title']
    user_id = session.get('user_id')  # Pega o ID do usuário logado
    add_task(title, user_id)
    return redirect('/mytasks')

@app.route('/remove_task/<int:task_id>', methods=['POST'])
@login_required
def remove_task_route(task_id):
    remove_task(task_id)
    return redirect('/mytasks')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        message = register_user(username, password, email, nome)

        if message == 'Usuário cadastrado com sucesso!':
            return render_template('login.html')
        else:
            return render_template('register.html', message=message)

    return render_template('register.html', message=None)

@app.route('/login', methods=['GET', 'POST'])
def login_user_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = login_user(username, password)

        if user:
            session['nome'] = user['nome']
            session['username'] = username  # Define o username na sessão
            session['user_id'] = user['id_user']  # Define o id_user na sessão
            session['is_admin'] = user.get('is_admin', False)  # Define se o usuário é admin
            return redirect('/mytasks')  # Redireciona para a página de tarefas
        else:
            flash('Nome de usuário ou senha incorretos.', category='incorreto')
            return redirect(url_for('login'))

    return render_template('login.html')  # Retorna a página de login

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove o usuário da sessão
    session.pop('user_id', None)  # Remove o ID do usuário da sessão
    session.pop('is_admin', None)  # Remove a informação se o usuário é admin
    flash('Você saiu com sucesso!', category='success')
    return redirect(url_for('login'))  # Redireciona para a página de login

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')

        with open(CAMINHO_USER, 'r') as arquivo:
            users = json.load(arquivo)
            user = next((user for user in users if user['email'] == email), None)

            if user:
                # Envia e-mail com o novo link
                enviar_email_recuperacao(email, email)
                flash('E-mail de recuperação enviado com sucesso!', 'success')
                return redirect(url_for('login'))
            else:
                flash('E-mail não encontrado. Verifique e tente novamente.', 'danger')
    return render_template('recovery.html')

@app.route('/redefinir-senha', methods=['GET', 'POST'])
def redefinir_senha():
    dados_criptografados = request.args.get('dados')
    error_message = None
    success_message = None
    email = None  # Inicializa a variável email

    if dados_criptografados and fernet:  # Verifica se o Fernet foi inicializado
        # Descriptografar os dados
        try:
            dados_descriptografados = fernet.decrypt(dados_criptografados.encode())
            # Aqui você precisa garantir que o email e o código estejam em formato adequado
            dados = dados_descriptografados.decode()  # Decodificando os dados descriptografados
            # Supondo que o email e o código sejam passados em formato "email&codigo"
            for param in dados.split('&'):
                chave, valor = param.split('=')
                if chave == 'email':
                    email = valor
                # Adicione qualquer outro parâmetro que você esteja passando

        except Exception as e:
            error_message = "Link inválido ou expirado."
            print(f"Erro na descriptografia: {e}")
            return render_template('resetpassword.html', error_message=error_message)

    if request.method == 'POST':
        nova_senha = request.form['nova_senha']
        confirmar_senha = request.form['confirm_password']

        if nova_senha != confirmar_senha:
            error_message = "As senhas não coincidem."
            return render_template('resetpassword.html', email=email, error_message=error_message)

        # Atualização da nova senha
        hashed_password = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
        with open(CAMINHO_USER, 'r+') as arquivo:
            users = json.load(arquivo)
            for user in users:
                if user['email'] == email:
                    user['password'] = hashed_password.decode('utf-8')
                    break
            arquivo.seek(0)
            json.dump(users, arquivo, indent=4)
            arquivo.truncate()

        success_message = "Senha redefinida com sucesso!"
        flash(success_message, category='success')
        return redirect(url_for('login'))

    return render_template('resetpassword.html', email=email, error_message=error_message)