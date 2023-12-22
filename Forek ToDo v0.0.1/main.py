from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)


@app.route('/')
def index():
  tasks = Task.query.all()
  return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
  content = request.form.get('content')
  if content:
    new_task = Task(content=content)
    db.session.add(new_task)
    db.session.commit()
  return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
  task = Task.query.get(task_id)
  if task:
    db.session.delete(task)
    db.session.commit()
  return redirect(url_for('index'))


# if __name__ == '__main__':
#   with app.app_context():
#     db.create_all()
#   app.run(host='0.0.0.0', port=8080)


@app.route('/api/tasks', methods=['GET'])
def get_tasks_api():
  tasks = Task.query.all()
  task_list = [{'id': task.id, 'content': task.content} for task in tasks]
  return jsonify(task_list)


if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(host='0.0.0.0', port=8080)
