import bcrypt
import json
from pathlib import Path

CAMINHO_USER = Path(__file__).parent / 'data' / 'users.json'

def ensure_users_file_exists():
    """Cria o arquivo users.json se ele não existir e inicializa com uma lista vazia."""
    if not CAMINHO_USER.exists():
        with open(CAMINHO_USER, 'w') as file:
            json.dump([], file)  # Inicializa como uma lista vazia

def get_next_id(users):
    """Retorna o próximo ID disponível, começando do 1."""
    if not users:  # Se não houver usuários, o próximo ID é 1
        return 1
    else:
        return max(user.get('id_user', 0) for user in users) + 1  # Usando 'id_user'

def register_user(username, password, email, nome, is_admin=False):
    ensure_users_file_exists()  # Garantir que o arquivo exista

    with open(CAMINHO_USER, 'r') as file:
        users = json.load(file)

    # Verifica se o usuário já existe
    for user in users:
        if user['title'] == username:
            return 'Usuário já cadastrado'
        
        elif user['email'] == email:
            return 'Email já cadastrado'
        
        elif user['title'] == username and user['email'] == email:
            return 'Usuário e Email já cadastrados'
        
    
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_user = {
        'id_user': get_next_id(users),
        'nome': nome,  # Obtém o próximo ID disponível
        'title': username,
        'password': password_hash.decode('utf-8'),
        'email': email,
        'is_admin': is_admin, # Adicionando o campo is_admin 
    }
    users.append(new_user)

    # Atualiza o arquivo com a nova lista de usuários
    with open(CAMINHO_USER, 'w') as file:
        json.dump(users, file, indent=4)

    return 'Usuário cadastrado com sucesso!'

def login_user(username, password):
    ensure_users_file_exists()  # Garantir que o arquivo exista

    with open(CAMINHO_USER, 'r') as file:
        users = json.load(file)

    for user in users:
        if user['title'] == username:
            # Verifica se a senha corresponde
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                return user  # Retorna o usuário se o login for bem-sucedido
            else:
                return None  # Senha incorreta
    return None  # Usuário não encontrado

def logout_user():
    """Função de logout."""
    return None  # O logout em si é tratado pela remoção da sessão na rota

if __name__ == '__main__':
    print(CAMINHO_USER)