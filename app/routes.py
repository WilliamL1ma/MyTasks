from flask import render_template, request, redirect, flash, session, url_for
from app import app
from app.tasks_manager import add_task, view_tasks, remove_task, view_old_tasks
from app.auth import register_user, login_user
from app.decorators import login_required

# Configuração da chave secreta para as sessões
app.secret_key = 'bomdia'

# Lista para armazenar usuários logados
logged_users = []

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
        username = request.form['username']
        password = request.form['password']
        message = register_user(username, password)

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

        # Verifica se o usuário já está logado
        if user and username in logged_users:
            flash('Este usuário já está logado em outro dispositivo.')
            return redirect(url_for('login'))

        if user:
            session['username'] = username  # Define o username na sessão
            session['user_id'] = user['id_user']  # Define o id_user na sessão
            session['is_admin'] = user.get('is_admin', False)  # Define se o usuário é admin
            logged_users.append(username)  # Adiciona o usuário à lista de logados
            return redirect('/mytasks')  # Redireciona para a página de tarefas
        else:
            flash('Nome de usuário ou senha incorretos.')

    return render_template('login.html')  # Retorna a página de login

@app.route('/logout', methods=['POST'])
def logout():
    username = session.get('username')
    if username in logged_users:
        logged_users.remove(username)  # Remove o usuário da lista de logados
    session.pop('username', None)  # Remove o usuário da sessão
    session.pop('user_id', None)  # Remove o ID do usuário da sessão
    session.pop('is_admin', None)  # Remove a informação se o usuário é admin
    flash('Você saiu com sucesso!')
    return redirect(url_for('login'))  # Redireciona para a página de login

