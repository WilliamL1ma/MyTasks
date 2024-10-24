from flask import render_template, request, redirect, flash
from app import app
from app.tasks_manager import add_task, view_tasks, remove_task
from app.auth import register_user, login_user

@app.route('/')
def login():
    return render_template('login.html')  # Retorna a página de login

@app.route('/mytasks', methods=['GET'])
def index():
    tasks = view_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task_route():
    title = request.form['title']
    add_task(title)
    return redirect('/mytasks')

@app.route('/remove_task/<int:task_id>', methods=['POST'])
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

        if user:
            return redirect('/mytasks')  # Redireciona para a página de tarefas
        else:
            flash('Nome de usuário ou senha incorretos.')

    return render_template('login.html')
