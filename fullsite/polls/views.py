from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .models import users
# Create your views here.


def signup(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            users.objects.create(user=user)
            login(request, user)
            return render( request, 'userlist.html')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        return render(request, 'signup.html')



def signin(request):
    if request.user.is_authenticated:
        return render(request, 'userlist.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return render( request, 'userlist.html')
        else:

            return render(request, 'signup.html')
    else:
        return render(request, 'signin.html')

def signout(request):
    logout(request)
    return redirect('signin')

def user_list(request):
    all_user = users.objects.all()
    return render (request, "userlist.html")