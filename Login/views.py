from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import CreateForm
from .models import Task

#@PassQ!Sam345
def home(requests):
    return render(requests, 'home.html')

def task(requests):
    task = Task.objects.filter(user= requests.user, datecomplete__isnull = True)
    return render(requests, 'task.html',
                  {"tasks": task}
                  )



def UserLogin(requests):
    
    if requests.method == "GET":
        return render(requests, "singin.html")
        
    elif requests.method == "POST":        
        form_recive = requests.POST

        #Password1 y password2 aparece unicamente cuando se registra un nuevo usuario
        if "password1" in form_recive:
            if form_recive["password1"] == form_recive["password2"]:
                try:
                    print(f"Se ha creado un nuevo user {requests.POST}")
                    user = User.objects.create_user(
                        username = requests.POST["email"], 
                        password= requests.POST["password1"]
                        )
                    user.save()
                    
                    login(requests, user)
                    return redirect("task")

                except:
                    return render(requests, "singin.html",{
                        "error": "El usuario ya existe"
                    })
            else:
                return render(requests, "singin.html",{
                        "error": "Las contraseñas no coinciden"
                    })
            
        #password es para los forms de login
        elif "password" in form_recive:
            user = authenticate(
                requests, 
                username = form_recive["email"], 
                password = form_recive["password"]
                )
            if user:
                login(requests, user)
                return redirect("task")
                
            else:
                return render(requests, "singin.html",{
                        "error": "El mail o la constraseña no son correctas"
                    })


def CloseSession(requests):
    logout(requests)
    return redirect("home")






def newtask(requests):
    if requests.method == "GET":
        return render(requests, "newtask.html", {
            "form": CreateForm
        })
        
    elif requests.method == "POST":        
        try:
            form = CreateForm(requests.POST)
            NewForm = form.save(commit=False)
            NewForm.user = requests.user
            NewForm.save()

            return render(requests, "task.html", {
                "form": CreateForm
            })
        except Exception as e:
            return render(requests, "task.html",{
                "error": "Revisa los datos ingresados"
                })