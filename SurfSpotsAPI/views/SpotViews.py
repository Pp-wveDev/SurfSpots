from bson import ObjectId

from django.shortcuts import render
from django.http import Http404

from pymongo.errors import DuplicateKeyError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from SurfSpotsAPI.models import Spot
from SurfSpotsAPI.serializers import SpotSerializer


class SpotBasic(APIView):
    def get_object(self, pk):
        try:
            pk = ObjectId(pk)
            return Spot.objects.get(pk=pk)
        except Spot.DoesNotExist:
            raise Http404
    
    @swagger_auto_schema(operation_id='List spots',
                         responses={200: 'Spots'})
    def get(self, request, pk=None):
        """ Return all the spots """
        spots = Spot.objects.all()
        serializer = SpotSerializer(spots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(responses= {201: 'Spot created',
                                     400: 'Error causes',
                                     409: 'Spots already exists'},
                         request_body= openapi.Schema(
                             title="Spot",
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'name': openapi.Schema(type=openapi.TYPE_STRING),
                                 'breakType': openapi.Schema(type=openapi.TYPE_STRING),
                             }
                         ), operation_id='Create new spot')
    def post(self, request):
        """ Creates a new Spot """
        serializer = SpotSerializer(data=request.data)
        
        try:
            if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except DuplicateKeyError:
            return Response('Spot already exists', status=status.HTTP_409_CONFLICT)
    
    @swagger_auto_schema(operation_id='Delete spots',
                         responses={204: 'Ok'})
    def delete(self, request):
        """Delete all the spots (Use with caution)"""
        spots = Spot.objects.all()
        spots.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)