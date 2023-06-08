from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '894ad1df46d08f691c788a0e3a5d1701'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('successful.html')


# class to store user info
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(80), unique=True, nullable=False)


# Class to store created tasks
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    due_date = db.Column(db.String(80))
    priority = db.Column(db.String(20))
    labels = db.Column(db.String(200))

    def __init__(self, title, description, due_date, priority, labels):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.labels = labels

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        Email = request.form['Email']
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('login'))

        # Create a new user
        user = User(username=username, password=password,Email=Email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return render_template('successful.html')
        else:
            return 'Invalid username or password'
    return render_template('login.html')


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        title = request.form['taskTitle']
        description = request.form['taskDescription']
        due_date = request.form['taskDueDate']
        priority = request.form['taskPriority']
        labels = request.form['taskLabels']

        task = Task(title=title, description=description, due_date=due_date, priority=priority, labels=labels)
        db.session.add(task)
        db.session.commit()

    tasks = Task.query.all()
    return render_template('taskhub.html', tasks=tasks)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

