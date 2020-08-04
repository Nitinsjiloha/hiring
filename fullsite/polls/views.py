import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from .models import users
LOG_FILENAME = 'loginfo.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

# Create your views here.

@csrf_exempt
def signup(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            users.objects.create(user=user)
            logging.info("New User Signed Up {}".format(username))
            login(request, user)
            return render( request, 'signin.html')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        return render(request, 'signup.html')


@csrf_exempt
def signin(request):
    # if request.user.is_authenticated:
    #     return render(request, 'userlist.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            all_user = users.objects.all()
            if all_user is not None:
                return render(request, "userlist.html", {'results': all_user})
            else:
                return render(request, 'signup.html')
        else:
            return render(request, 'signup.html')
    else:
        return render(request, 'signin.html')

@csrf_exempt
def signout(request):
    logout(request)
    return redirect('signin')


def delete(request):
    id = request.POST['userID']
    if request.method == "POST":
        obj = users.objects.filter(id=id)
        obj.delete()
        all_user = users.objects.all()
        return render("userlist.html", {'results': all_user})
    return render(request, "signin.html")
