from django.urls import path
from django.conf.urls import url,include

from SurfSpotsWeb.views.UserViews import *

urlpatterns = [
    path('user/', load_UserList, name="loadUsers"),
    path('user/<str:pk>/delete', delete_User, name="deleteUser"),
    path('user/<str:pk>/update', update_User, name="updateUser"),
    path('newUser/', create_User, name="createUser"),
]