from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:  # Verifica se o usuário está logado
            flash('Você precisa estar logado para acessar essa página.', category='danger')
            return redirect(url_for('login'))  # Redireciona para a página de login
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_admin' not in session or not session['is_admin']:  # Verifica se o usuário é admin
            flash('Acesso negado. Você não tem permissão para acessar esta página.', category='danger')
            return redirect(url_for('index'))  # Redireciona para a página de tarefas
        return f(*args, **kwargs)
    return decorated_function
