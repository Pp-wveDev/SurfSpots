from django.shortcuts import render, redirect
from django.template import Context
from django.http import HttpRequest, HttpResponseRedirect

from SurfSpotsWeb.forms import UserForm
from SurfSpotsAPI.serializers import UserSerializer
from SurfSpotsAPI.models import User
from .util.UserUtil import *

def load_UserList(request):
    users = getUsers()
    context = { 'users' : users }
    
    return render(request, 'userList.html', context=context)

def delete_User(request, pk):
    deleteUser(pk)
    
    return redirect('loadUsers')

def update_User(request, pk):
    user = getUser(pk)
    
    form = UserForm(initial={'username': user['username'],
                             'email': user['email'],
                             'name': user['name'],
                             'password': user['password'],
                             'bio': user['bio']})
    
    if request.method == "POST":
        form = UserForm(request.POST)
        
        if form.is_valid():
            user.update(username=request.POST.get('username'),
                        email=request.POST.get('email'),
                        name=request.POST.get('name'),
                        password=request.POST.get('password'),
                        bio=request.POST.get('bio'))
            updateUser(user['id'], user)
            
            return redirect('loadUsers')

    context = {'form': form}
    return render(request, 'userUpdate.html', context)

def create_User(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        
        if form.is_valid():
            user= {"username":request.POST.get('username'),
                   "email":request.POST.get('email'),
                   "name":request.POST.get('name'),
                   "password":request.POST.get('password'),
                   "bio":request.POST.get('bio')}
            createUser(user)
            
            return redirect('loadUsers')

    form = UserForm()
    context = {'form': form}
    
    return render(request, 'userCreate.html', context)