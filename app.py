from flask import request, jsonify, Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@localhost/{os.getenv('MYSQL_DATABASE')}"
db = SQLAlchemy(app)

# with app.app_context():
#     db.create_all()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.route('/tasks', methods=['GET', 'POST'])
def tasks_endpoints():
    if request.method == 'POST':
        title = request.form.get('title')
        if not title:
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
def task_endpoints(id):
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


if __name__ == '__main__':
    app.run(debug=True)
