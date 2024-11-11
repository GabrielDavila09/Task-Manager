from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Modelo de Usuario
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

# Modelo de Tarea
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name='fk_task_user_id'),  # Añade un nombre a la clave foránea
        nullable=True
    )
    comments = db.relationship('Comment', back_populates='task')
    tags = db.relationship('Tag', secondary='task_tag', back_populates='tasks')

# Modelo de Comentario
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    task_id = db.Column(
        db.Integer,
        db.ForeignKey('task.id', name='fk_comment_task_id'),  # Añade un nombre a la clave foránea
        nullable=False
    )
    task = db.relationship('Task', back_populates='comments')

# Modelo de Etiqueta
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    tasks = db.relationship('Task', secondary='task_tag', back_populates='tags')

# Tabla de asociación para la relación many-to-many entre Task y Tag
task_tag = db.Table('task_tag',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id', name='fk_task_tag_task_id')),  # Añade un nombre a la clave foránea
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', name='fk_task_tag_tag_id'))  # Añade un nombre a la clave foránea
)
