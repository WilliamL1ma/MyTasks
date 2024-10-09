import json
import os

# Caminho do arquivo JSON
TASKS_FILE = 'tasks.json'

# Carregar tarefas do arquivo JSON
def load_tasks(filename=TASKS_FILE):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []  # Retorna lista vazia se o arquivo não existir

# Salvar tarefas no arquivo JSON
def save_tasks(tasks, filename=TASKS_FILE):
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=4)

# Adicionar nova tarefa
def add_task(title):
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,  # Gera um novo ID
        "title": title,
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task

# Ver tarefas
def view_tasks():
    return load_tasks()

# Remover tarefa
def remove_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
