document.addEventListener('DOMContentLoaded', function () {
    var taskForm = document.getElementById('taskForm');
    var taskList = document.getElementById('taskList');

    taskForm.addEventListener('submit', function (event) {
        event.preventDefault();

        var taskTitle = document.getElementById('taskTitle').value;
        var taskDescription = document.getElementById('taskDescription').value;
        var taskDueDate = document.getElementById('taskDueDate').value;
        var taskPriority = document.getElementById('taskPriority').value;
        var taskLabels = document.getElementById('taskLabels').value;

        createTask(taskTitle, taskDescription, taskDueDate, taskPriority, taskLabels);

        taskForm.reset();
    });

    function createTask(title, description, dueDate, priority, labels) {
        var task = document.createElement('div');
        task.classList.add('task');

        var taskTitle = document.createElement('h3');
        taskTitle.textContent = title;

        var taskDescription = document.createElement('p');
        taskDescription.textContent = description;

        var taskDueDate = document.createElement('p');
        taskDueDate.textContent = 'Due Date: ' + dueDate;

        var taskPriority = document.createElement('p');
        taskPriority.textContent = 'Priority: ' + priority;

        var taskLabels = document.createElement('p');
        taskLabels.textContent = 'Labels: ' + labels;

        task.appendChild(taskTitle);
        task.appendChild(taskDescription);
        task.appendChild(taskDueDate);
        task.appendChild(taskPriority);
        task.appendChild(taskLabels);

        taskList.appendChild(task);
    }
});

