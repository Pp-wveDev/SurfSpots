from mongodbforms import DocumentForm
from mongoengine import *

from django.db import models

from SurfSpotsAPI.models import User

class UserForm(DocumentForm):
    class Meta:
        document = User
        fields = ['username', 'email', 'name', 'bio', 'password']