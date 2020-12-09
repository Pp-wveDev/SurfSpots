from bson import ObjectId

from django.shortcuts import render
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from SurfSpotsAPI.models import User
from SurfSpotsAPI.serializers import UserSerializer

class UserBasic(APIView):
    @swagger_auto_schema(operation_id='List users',
                         responses={200: 'Users'})
    def get(self, request, pk=None):
        """Returns all the users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(responses= {201: 'User created',
                                     400: 'Error causes'},
                         request_body= openapi.Schema(
                             title="User",
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'username': openapi.Schema(type=openapi.TYPE_STRING),
                                 'email': openapi.Schema(type=openapi.TYPE_STRING),
                                 'password': openapi.Schema(type=openapi.TYPE_STRING),
                             }),
                         operation_id='Create new user')
    def post(self, request):
        """ Creates a new User """
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(operation_id='Delete users',
                         responses={204: ''})
    def delete(self, request):
        """Delete all the users (Use with caution)"""
        users = User.objects.all()
        users.delete()
        
        return Response({'message': 'all the users were deleted'},status=status.HTTP_204_NO_CONTENT)
    
class UserDetail(APIView):
    def getObject(self, pk):
        try:
            pk = ObjectId(pk)
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
    
    
    @swagger_auto_schema(operation_id="Get an user",
                         responses={200: 'User requested',
                                    422: 'User not found',
                                    400: 'Error'})
    def get(self, request, pk=None):
        """Returns the user with the id given"""
        if pk:
            pk = ObjectId(pk)
            user = self.getObject(pk)
            
            if user:
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            else: # User not found
                return Response("User not found", status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(operation_id="Delete an user",
                         responses={204: 'User deleted',
                                    422: 'User not found',
                                    400: 'Bad request'})
    def delete(self, request, pk=None):
        """ Deletes the user with the id given """
        if pk:
            pk = ObjectId(pk)
            user = self.getObject(pk)
            
            if user:
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
                
            else:
                return Response("User not found", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(operation_id='Modify user',
                            responses={202: 'User modified',
                                    422: 'User not found',
                                    400: 'Bad request'},
                        request_body=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'password': openapi.Schema(type=openapi.TYPE_STRING),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                                'bio': openapi.Schema(type=openapi.TYPE_STRING)
                            }
    ))
    def put(self, request, pk):
        """ Modifies the user with the id given """
        pk = ObjectId(pk)
        user = self.getObject(pk)
        
        if user:
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            
            else: # Not a valid modification
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        else: # User not found
            return Response("User not found", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class UserByName(APIView):
    @swagger_auto_schema(operation_id='Get user by username',
                     responses={200: 'Users',
                                400: 'No username given'}
                    )
    def get(self, request, username=None):
        """Retrieve all the users with the username given"""
        if username:
            users = User.objects.filter(username__contains=username)
            serializer = UserSerializer(users, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response("No username given", status=status.HTTP_400_BAD_REQUEST)
            