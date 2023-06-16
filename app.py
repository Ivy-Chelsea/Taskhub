from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

app = Flask(__name__)

# Set secret key for app
app.secret_key = '894ad1df46d08f691c788a0e3a5d1701'

# Set database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Create SQLAlchemy database object
db = SQLAlchemy(app)

# Define User class to store user information
class User(db.Model, UserMixin):
    """
    A class used to represent a user in the database.
    """

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, first_name, last_name, username, password, email):
        """
        Initializes a new instance of the User class.
        """

        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email


# Define Task class to store created tasks
class Task(db.Model):
    """
    A class used to represent a task in the database.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    due_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    reminder_date = db.Column(db.Date)
    priority = db.Column(db.String(10), nullable=False)
    labels = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, description, due_date, start_time, end_time, reminder_date, priority, labels, user_id):
        """
        Initializes a new instance of the Task class.
        """

        self.title = title
        self.description = description
        self.due_date = due_date
        self.start_time = start_time
        self.end_time = end_time
        self.reminder_date = reminder_date
        self.priority = priority
        self.labels = labels
        self.user_id = user_id

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'

# Create login manager object
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('landing_page'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Renders the registration page if the user is not logged in, otherwise redirects to the task page.
@app.route('/')
def index():
    
    if current_user.is_authenticated:
        return render_template('landing.html')
    else:
        return render_template('landing.html')

@app.route('/landing')
def landing_page():
    return render_template('landing.html')

@app.route('/successful')
def successful():
    return render_template('successful.html')


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']

        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return redirect(url_for('settings'))
        
        if not first_name:
            flash('First name is required', 'danger')
        elif not last_name:
            flash('Last name is required', 'danger')
        elif not email:
            flash('Email is required', 'danger')
        elif password != confirm_new_password:
            flash('Passwords do not match', 'danger')
        else:
            # Check if email already exists for a different user
            existing_user = User.query.filter(User.email == email, User.id != current_user.id).first()
            if existing_user:
                flash('Email address already exists', 'error')
                return redirect(url_for('settings'))

            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.email = email
            if password:
                current_user.password = generate_password_hash(password)
            db.session.commit()
            flash('Your settings have been updated', 'success')
            return redirect(url_for('settings'))

    return render_template('settings.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    """
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

         # Validate the password
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return redirect(url_for('register'))

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('The username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('The email address already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        # Create a new user
        new_user = User(first_name=first_name, last_name=last_name, username=username, password=generate_password_hash(password), email=email)
        db.session.add(new_user)
        db.session.commit()

        # Log the user in and redirect to the home page
        login_user(new_user)
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the user by username
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('successful'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

# Handles task creation. 
@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        title = request.form.get('tasktitle')
        description = request.form.get('taskDescription')
        due_date = datetime.strptime(request.form.get('taskDueDate'), '%Y-%m-%d').date()
        start_time = datetime.strptime(request.form.get('taskStartTime'), '%H:%M').time()
        end_time = datetime.strptime(request.form.get('taskEndTime'), '%H:%M').time()
        reminder_date = datetime.strptime(request.form.get('taskReminderDate'), '%Y-%m-%d').date() if request.form.get('taskReminderDate') else None
        priority = request.form.get('taskPriority')
        labels = request.form.get('taskLabels')
        user_id = current_user.id

        # Create a new task
        new_task = Task(title=title, description=description, due_date=due_date, start_time=start_time, end_time=end_time, reminder_date=reminder_date, priority=priority, labels=labels, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()

        flash('Task created!', 'success')
        return redirect(url_for('tasks'))
    return render_template('Todo.html')


@app.route('/tasks/<int:task_id>/edit', methods=['POST', 'GET'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        task.title = request.form['tasktitle']
        task.description = request.form['taskDescription']
        task.due_date = request.form['taskDueDate']
        task.start_time = request.form['taskStartTime']
        task.end_time = request.form['taskEndTime']
        task.reminder_date = request.form['taskReminderDate']
        task.priority = request.form['taskPriority']
        task.labels = request.form['taskLabels']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_task.html', task=task)



@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('index'))


#Handles user logout.
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('landing.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)