import json
import os
import time
from pathlib import Path

# Caminho dos arquivos JSON
TASKS_FILE = Path(__file__).parent / 'data' / 'tasks.json'
ID_REGISTER = Path(__file__).parent / 'data' / 'register_id.json'
OLD_TASKS = Path(__file__).parent / 'data' / 'old_tasks.json'

def ensure_tasks_file_exists():
    """Cria o arquivo tasks.json se ele não existir e inicializa com uma lista vazia."""
    if not TASKS_FILE.exists():
        with open(TASKS_FILE, 'w') as file:
            json.dump([], file)

def ensure_old_tasks_file_exists():
    """Cria o arquivo old_tasks.json se ele não existir e inicializa com uma lista vazia."""
    if not OLD_TASKS.exists():
        with open(OLD_TASKS, 'w') as file:
            json.dump([], file)

def load_tasks(filename=TASKS_FILE):
    ensure_tasks_file_exists()  # Garantir que o arquivo exista
    with open(filename, 'r') as file:
        return json.load(file)

def save_tasks(tasks, filename=TASKS_FILE):
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=4)

def load_register_id(file_id=ID_REGISTER):
    if os.path.exists(file_id):
        try:
            with open(file_id, 'r') as file:
                arq = json.load(file)
                if isinstance(arq, dict) and 'max_id' in arq:
                    return arq['max_id']
        except json.JSONDecodeError:
            pass
    return 1  # Se o arquivo não existir ou estiver corrompido, começa em 1

def save_register_id(new_id, file_id=ID_REGISTER):
    with open(file_id, 'w') as file:
        json.dump({"max_id": new_id}, file, indent=4)

def add_task(title, user_id):
    ensure_tasks_file_exists()  # Garantir que o arquivo exista
    tasks = load_tasks()

    # Carrega o próximo ID único
    id_max = load_register_id()

    new_task = {
        "id_task": id_max,  # ID da tarefa
        "title": title,
        "completed": False,
        "user_id": user_id,  # ID do usuário que criou a tarefa
        "created_at": time.time()
    }
    tasks.append(new_task)

    # Atualiza o registro de ID com o novo valor máximo
    save_register_id(id_max + 1)

    save_tasks(tasks)
    return new_task

def view_tasks(user_id):
    tasks = load_tasks()
    return [task for task in tasks if task.get("user_id") == user_id]  # Usa get para evitar KeyError

def remove_task(task_id):
    tasks = load_tasks()
    old_tasks = load_old_tasks()

    # Filtra e encontra a tarefa a ser removida
    task_to_remove = None  # Variável para armazenar a tarefa a ser removida
    for task in tasks:
        if task.get("id_task") == task_id:
            task_to_remove = task
            break  # Sai do loop assim que a tarefa é encontrada

    if task_to_remove:
        # Adiciona a tarefa removida ao arquivo de tarefas antigas
        old_tasks.append(task_to_remove)
        save_old_tasks(old_tasks)

        # Remove a tarefa da lista original
        tasks = [task for task in tasks if task.get("id_task") != task_id]
        save_tasks(tasks)

def load_old_tasks(filename=OLD_TASKS):
    ensure_old_tasks_file_exists()  # Garantir que o arquivo exista
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []  # Retorna lista vazia se o arquivo não existir

def save_old_tasks(old_tasks, filename=OLD_TASKS):
    with open(filename, 'w') as file:
        json.dump(old_tasks, file, indent=4)

def view_old_tasks(user_id):
    old_tasks = load_old_tasks()
    current_time = time.time()

    # Filtra tarefas antigas por usuário e pelo tempo de criação
    return [
        task for task in old_tasks 
        if task.get("user_id") == user_id and (current_time - task.get('created_at', 0)) 
    ]

