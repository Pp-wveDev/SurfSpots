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

from SurfSpotsAPI.models import Review, Spot
from SurfSpotsAPI.serializers import ReviewSerializer
from SurfSpotsAPI.views.SpotViews import SpotBasic

# Custom queries: https://docs.mongoengine.org/guide/querying.html

class ReviewBasic(APIView):
    def getReview(self, spk):
        try:
            spk = ObjectId(spk)
            spots = Spot.objects.get(pk=spk)
            reviews = spots.reviewList
            
            return reviews
        
        except Spot.DoesNotExist:
            return None
    
    def get(self, request, spk):
        """ Retrieves all the reviews made to the selected spot """
        spk = ObjectId(spk)
        
        if spk:
            reviews = self.getReview(spk)
            
            serializer = ReviewSerializer(reviews, many=True)
        
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_id='New review',
                         responses={202: 'Review created',
                                    422: 'Spot not found',
                                    400: 'Bad request'},
                         request_body= ReviewSerializer)
    def post(self, request, spk):
        serializer = ReviewSerializer(data=request.data)
        spot = SpotBasic.get_object(request, spk)
        
        if spot: # Spot found
            if serializer.is_valid(): # Correct review
                spot.reviewList.append(serializer.save())
                spot.save()
                
                # Save spot on User.reviews_made
                if spot not in serializer.instance.user_author.reviews_made:
                    serializer.instance.user_author.reviews_made.append(spot)
                    serializer.instance.user_author.save()
            
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else: # Bad review
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else: # Spot not found
            return Response("Spot not found", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    def delete(self, request, spk):
        spk = ObjectId(spk)
        
        spot = SpotBasic.get_object(request, spk)
        reviews = self.getReview(spk)
        
        for review in reviews: # For each review
            # Remove appereance on authors
            review.user_author.reviews_made.remove(spot)
            review.user_author.save()
            
            # Remove from spot
            spot.reviewList.remove(review)
            spot.save()
        
        return Response(status.HTTP_200_OK)
        