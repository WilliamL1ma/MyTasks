import json
import os

# Caminho dos arquivos JSON
TASKS_FILE = 'tasks.json'
ID_REGISTER = 'register_id.json'
OLD_TASKS = 'old_tasks.json'

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

# Carregar o próximo ID único do arquivo JSON
def load_register_id(file_id=ID_REGISTER):
    if os.path.exists(file_id):
        try:
            with open(file_id, 'r') as file:
                data = json.load(file)
                if isinstance(data, dict) and 'max_id' in data:
                    return data['max_id']
        except json.JSONDecodeError:
            pass
    return 1  # Se o arquivo não existir ou estiver corrompido, começa em 1

# Salvar o próximo ID único no arquivo JSON
def save_register_id(new_id, file_id=ID_REGISTER):
    with open(file_id, 'w') as file:
        json.dump({"max_id": new_id}, file, indent=4)

# Carregar tarefas removidas do arquivo JSON
def load_old_tasks(filename=OLD_TASKS):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []  # Retorna lista vazia se o arquivo não existir

# Salvar tarefas removidas no arquivo JSON
def save_old_tasks(old_tasks, filename=OLD_TASKS):
    with open(filename, 'w') as file:
        json.dump(old_tasks, file, indent=4)

# Adicionar nova tarefa
def add_task(title):
    tasks = load_tasks()

    # Carrega o próximo ID único
    id_max = load_register_id()

    new_task = {
        "id": id_max,  # Usa o próximo ID único
        "title": title,
        "completed": False
    }
    tasks.append(new_task)

    # Atualiza o registro de ID com o novo valor máximo
    save_register_id(id_max + 1)

    save_tasks(tasks)
    return new_task

# Ver tarefas
def view_tasks():
    return load_tasks()

# Remover tarefa e salvar no arquivo de removidas
def remove_task(task_id):
    tasks = load_tasks()
    old_tasks = load_old_tasks()

    # Filtra e encontra a tarefa a ser removida
    task_to_remove = [task for task in tasks if task["id"] == task_id]

    if task_to_remove:
        # Adiciona a tarefa removida ao arquivo de tarefas antigas
        old_tasks.extend(task_to_remove)
        save_old_tasks(old_tasks)

        # Remove a tarefa da lista original
        tasks = [task for task in tasks if task["id"] != task_id]
        save_tasks(tasks)
