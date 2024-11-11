from flask import Flask, render_template, request, redirect, url_for
from models import db, Task, Comment, User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Inicialización de Flask-Migrate
migrate = Migrate(app, db)

# Inicialización del LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Implementar la lógica de inicio de sesión aquí
    pass

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    tasks = Task.query.all()
    now = datetime.now()
    for task in tasks:
        if task.due_date and task.due_date < now and not task.completed:
            task.alert = True  # Usar una variable o lógica para alertas
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_title = request.form['title']
    new_task = Task(title=task_title)
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

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/assign/<int:task_id>/<int:user_id>')
def assign_task(task_id, user_id):
    task = Task.query.get(task_id)
    user = User.query.get(user_id)
    if task and user:
        task.user_id = user_id
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/comment/<int:task_id>', methods=['POST'])
def add_comment(task_id):
    content = request.form['content']
    comment = Comment(content=content, task_id=task_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    tasks = Task.query.filter(Task.title.contains(query)).all()
    return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
