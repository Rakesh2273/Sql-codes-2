# models.py
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

# views.py
from django.shortcuts import render, redirect
from .models import Task

def index(request):
    tasks = Task.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        new_task = Task(title=title)
        new_task.save()
        return redirect('/')
    return render(request, 'index.html', {'tasks': tasks})

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('/')

def update_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('/')
    return render(request, 'update.html', {'task': task})

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
]

# index.html
<!DOCTYPE html>
<html>
<head>
    <title>To-Do List</title>
</head>
<body>
    <h1>To-Do List</h1>
    <form method="POST">
        {% csrf_token %}
        <input type="text" name="title" placeholder="New Task">
        <button type="submit">Add</button>
    </form>
    <ul>
        {% for task in tasks %}
            <li>{{ task.title }} <a href="{% url 'delete_task' task.id %}">Delete</a> <a href="{% url 'update_task' task.id %}">Update</a></li>
        {% endfor %}
    </ul>
</body>
</html>

# update.html
<!DOCTYPE html>
<html>
<head>
    <title>Update Task</title>
</head>
<body>
    <h1>Update Task</h1>
    <form method="POST">
        {% csrf_token %}
        <input type="text" name="title" value="{{ task.title }}">
        <input type="checkbox" name="completed" {% if task.completed %}checked{% endif %}> Completed
        <button type="submit">Update</button>
    </form>
</body>
</html>
