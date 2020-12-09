from rest_framework_mongoengine import serializers, fields as mFields

from rest_framework import fields
from .models import User, Spot, Review

class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ReviewSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class SpotSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Spot
        fields = '__all__'