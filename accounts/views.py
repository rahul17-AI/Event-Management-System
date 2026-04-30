from django.shortcuts import render,redirect
from accounts.forms import userForm, userProfileForm, UpdateForm,userDetailsUpdateForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from events.models import EventsList

# Create your views here.

def register(request):
    registered = False
    if request.method == 'POST':
        form = userForm(request.POST)
        form1 = userProfileForm(request.POST, request.FILES)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            profile = form1.save(commit=False) # profile we r saving form1 but not in backend
            profile.user = user # imp 
            profile.save()
            registered = True 
    else:
        form = userForm()
        form1 = userProfileForm()
    return render(request,"registration.html",{"form":form, "form1":form1, "registered": registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect('home')
        else:
            return HttpResponse('<h1> Please Check your Creds...')
        
    return render(request,"login.html")

@login_required(login_url='login')
def home(request):
    events = EventsList.objects.all()
    context = {
        'events' : events
    }
    return render(request,"home.html", context)

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def userprofile(request):
    return render(request,'userprofile.html')

@login_required(login_url='login')
def userUpdate(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=request.user)
        form1 = userDetailsUpdateForm(request.POST, request.FILES,instance=request.user.userdetails)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.save()

            profile = form1.save(commit = False)
            profile.user = user
            profile.save()
            return redirect('profile')
    else:
        form = UpdateForm(instance=request.user)
        form1 = userDetailsUpdateForm(instance=request.user.userdetails)
    return  render(request, "update.html", {'form':form,'form1':form1})