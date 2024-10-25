from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:  # Verifica se o usuário está logado
            flash('Você precisa estar logado para acessar essa página.')
            return redirect(url_for('login'))  # Redireciona para a página de login
        return f(*args, **kwargs)
    return decorated_function
