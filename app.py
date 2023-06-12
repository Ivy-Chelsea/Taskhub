from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)

# Set secret key for app
app.secret_key = '894ad1df46d08f691c788a0e3a5d1701'

# Set database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Create SQLAlchemy database object
db = SQLAlchemy(app)

@app.route('/landing')
def landing_page():
    return render_template('landing.html')


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
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    due_date = db.Column(db.String(80))
    priority = db.Column(db.String(20))
    labels = db.Column(db.String(200))

    def __init__(self, title, description, due_date, priority, labels):
        """
        Initializes a new instance of the Task class.
        """

        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.labels = labels


# Create login manager object
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    """
    Renders the registration page if the user is not logged in, otherwise redirects to the task page.
    """
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return render_template('index.html')

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
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Validate the email address
        if '@' not in email:
            flash('Invalid email address', 'error')
            return redirect(url_for('register'))

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


@app.route('/logout')
@login_required
def logout():
    """
    Handles user logout.
    """
    logout_user()
    return render_template('index.html')



@app.route('/tasks')
@login_required
def tasks():
    """
    Renders the task page.
    """
    tasks = Task.query.all()
    return render_template('Todo.html', tasks=tasks)


@app.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    """
    Handles task creation.
    """
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        priority = request.form['priority']
        labels = request.form['labels']

        # Create a new task
        new_task = Task(title=title, description=description, due_date=due_date, priority=priority, labels=labels)
        db.session.add(new_task)
        db.session.commit()

        flash('Task created!', 'success')
        return redirect(url_for('tasks'))

    return render_template('create_task.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
