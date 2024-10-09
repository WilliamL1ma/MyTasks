from flask import render_template, request, redirect
from app import app
from app.tasks_manager import add_task, view_tasks, remove_task

@app.route('/')
def index():
    tasks = view_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task_route():
    title = request.form['title']
    add_task(title)
    return redirect('/')

@app.route('/remove_task/<int:task_id>', methods=['POST'])
def remove_task_route(task_id):
    remove_task(task_id)
    return redirect('/')
