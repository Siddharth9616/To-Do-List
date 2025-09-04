from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from todo import models
from todo.models import TODOO
from django.contrib.auth import authenticate,login,logout
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method=='POST':
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('email')
        pwd=request.POST.get('pwd')               
        my_user=User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        return redirect('/login')
    return render(request, 'signup.html')
    

def login_view(request: HttpRequest):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        userr = authenticate(request, username=fnm, password=pwd)

        if userr is not None:
            login(request, userr)  # calling Django login
            return redirect('/todopage')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('/login')  

    return render(request, 'login.html')

@login_required(login_url='/login')
def todo(request):
    if request.method=='POST':
        title=request.POST.get('title')
        obj=models.TODOO(title=title, user=request.user)
        obj.save()
        messages.success(request, 'Task added successfully!')
        
        return redirect('/todopage')
    pending = TODOO.objects.filter(user=request.user, completed=False).order_by('-date')
    completed = TODOO.objects.filter(user=request.user, completed=True).order_by('-date')
    return render(request, 'todo.html', {
        'pending': pending,
        'completed': completed
    })

@login_required(login_url='/login')
def edit_todo(request, srno):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODOO.objects.get(srno=srno)
        obj.title = title
        obj.save()
        return redirect('/todopage')

    obj = models.TODOO.objects.get(srno=srno)
    return render(request, 'edit_todo.html', {'obj': obj})

@login_required(login_url='/login')    
def delete_todo(request, srno):
    obj = models.TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

@login_required(login_url='/login')
def toggle_task(request, srno):
    task = get_object_or_404(TODOO, srno=srno, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('/todopage')

@login_required(login_url='/login')
def clear_completed(request):
    models.TODOO.objects.filter(user=request.user, completed=True).delete()
    messages.success(request, "All completed tasks cleared!")
    return redirect('/todopage')

def signout(request):
    logout(request)
    return redirect('/login')