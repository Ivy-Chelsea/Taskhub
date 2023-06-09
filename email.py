from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app import *

@app.route('/Todo', methods=['GET', 'POST'])
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

        if due_date:
            for user in User.query.all():
                if user.Email:
                    from_email = 'your_email@example.com'
                    to_email = user.Email
                    subject = 'New Task with Due Date'
                    body = f'A new task has been added with the following details:\n\nTitle: {title}\nDescription: {description or "-"}\nDue Date: {due_date}\nPriority: {priority}\n'
                    message = MIMEMultipart()
                    message['From'] = from_email
                    message['To'] = to_email
                    message['Subject'] = subject
                    message.attach(MIMEText(body, 'plain'))
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(from_email, 'your_email_password')
                    server.sendmail(from_email, to_email, message.as_string())
                    server.quit()

    tasks = Task.query.all()

    today = datetime.date.today()
    tasks_due_today = Task.query.filter_by(due_date=today.strftime('%Y-%m-%d')).all()
    if tasks_due_today:
        for user in User.query.all():
            if user.Email:
                from_email = 'your_email@example.com'
                to_email = user.Email
                subject = 'Task Due Today'
                body = 'The following tasks are due today:\n\n'
                for task in tasks_due_today:
                    body += f'- {task.title}\n'
                message = MIMEMultipart()
                message['From'] ='your_email@example.com'
                message['To'] = to_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(from_email, 'your_email_password')
                server.sendmail(from_email, to_email, message.as_string())
                server.quit()

    return render_template('Todo.html', tasks=tasks)


if __name__ == '__main__':
    app.run(debug=True)
