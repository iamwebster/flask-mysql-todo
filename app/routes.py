from flask import request, jsonify
from app.database import db
from app import app 
from app.models import Task
from datetime import datetime


@app.route('/tasks', methods=['GET', 'POST'])
def tasks_endpoints():
    '''
    ### Эндпоинты для обработки задач.

    GET: Извлекает все задачи.
    POST: Создает новую задачу, указывая заголовок и, при необходимости, описание.

    Возвращается:
    - В случае успешного POST запроса: объект JSON с подробной информацией о созданной задаче.
    - В случае успешного GET запроса: массив JSON с подробной информацией обо всех задачах.
    - Если в POST запросе отсутствует заголовок: сообщение об ошибке с указанием требуемого поля.
    '''
    if request.method == 'POST':
        title = request.form.get('title')
        if not title or not isinstance(title, str):
            return {'Error!': 'Required field: title(string)'}
        
        data = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
        }
        
        task = Task(**data)
        db.session.add(task)
        db.session.commit()
        return jsonify(data)

    elif request.method == 'GET':
        tasks = Task.query.all()
        tasks_json = jsonify([task.to_json() for task in tasks])
        return tasks_json


@app.route('/tasks/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def task_endpoints(id: int):
    '''
    ### Эндпоинты для обработки отдельных задач по id.

    GET: Извлекает сведения о конкретной задаче по ее идентификатору.
    PUT: Обновляет сведения о конкретной задаче по ее идентификатору.
    DELETE: Удаляет конкретную задачу по ее идентификатору.

    Параметры:
    - id: int, идентификатор задачи, над которой нужно работать.

    Возвращается:
    - Если задача с указанным идентификатором не найдена: сообщение в формате JSON, указывающее, что задача не найдена.
    - В случае успешного GET запроса: объект в формате JSON с подробной информацией о задаче.
    - В случае успешного PUT запроса: объект в формате JSON  обновленными сведениями о задаче.
    - В случае успешного DELETE запроса: сообщение в формате JSON, указывающее на успешное удаление задачи.
    '''
    task = Task.query.get(id)

    if not task:
        return jsonify({'message': 'Task not found'}), 404

    if request.method == 'GET':
        return jsonify(task.to_json())

    elif request.method == 'PUT':
        task.title = request.form.get('title', task.title)
        task.description = request.form.get('description', task.description)
        task.updated_at = datetime.now()
        db.session.commit()
        return jsonify(task.to_json())

    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task was deleted successfully'})


with app.app_context():
    db.create_all()
    