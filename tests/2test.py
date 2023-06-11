from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)

# Set a secret key to use sessions
app.secret_key = '894ad1df46d08f691c788a0e3a5d1701'

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)


# Define the Task model
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


# Define the routes
@app.route('/')
def index():
    return render_template('register.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['Email']

        # Validate the email address
        if '@' not in email:
            flash('Invalid email address', 'error')
            return redirect(url_for('register'))

        # Validate the password
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return redirect(url_for('register'))

        # Check if the username or email address already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('login'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists', 'error')
            return redirect(url_for('register'))

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create a new user object and add it to the database
        user = User(username=username, password=hashed_password.decode('utf-8'), email=email)
        db.session.add(user)
        db.session.commit()

        # Store the user's username in the session
        session['username'] = username

        # Redirect to the tasks page
        flash(f'Welcome, {username}!', 'success')
        return redirect(url_for('login'))

    return render_template('successful.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        # Retrieve the user object from the database
        user = User.query.filter_by(username=username).first()
        if user:
            # Retrieve the hashed password from the database
            hashed_password = user.password.encode('utf-8')
            # Check if the hashed password matches the entered password
            if bcrypt.checkpw(password, hashed_password):
                # Store the user's username in the session
                session['username'] = username

                # Redirect to the tasks page
                flash(f'Welcome back, {username}!', 'success')
                return redirect(url_for('successful.html'))
            else:
                flash('Invalid username or password', 'error')
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Remove the username from the session
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['taskTitle']
        description = request.form['taskDescription']
        due_date = request.form['taskDueDate']
        priority = request.form['taskPriority']
        labels = request.form['taskLabels']

        # Create a new task object and add it to the database
        task = Task(title=title, description=description, due_date=due_date, priority=priority,labels=labels)
        db.session.add(task)
        db.session.commit()

    # Retrieve all tasks from the database
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)


if __name__ == '__main__':
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Start the Flask app
    app.run(debug=True, port=8000)
