from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key = '894ad1df46d08f691c788a0e3a5d1701'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(80), unique=True, nullable=False)
    task = db.Column(db.String(80),unique=True,  nullable=False)


    def __init__(self, Title,task):
        self.Title = Title
        self.task =task
    

@app.route("/") 
def fndex():
    return "hi "       
    

@app.route("/form",methods=['POST','GET']) 
def index():        
    if request.method == 'POST':
        Title = request.form['Title']
        task= request.form['task']
        Title1=Task(Title=Title,task=task)
        db.session.add(Title1)
        db.session.commit()
        

    tasks = Task.query.all()       
    return render_template('index.html')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

