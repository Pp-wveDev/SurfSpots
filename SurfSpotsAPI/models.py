from django.db import models

from mongoengine import Document, fields, EmbeddedDocument, PULL, CASCADE

class User(Document):
    username = fields.StringField(required=True, max_length=30)
    email = fields.EmailField(required=True)
    name = fields.StringField(max_length=50)
    password = fields.StringField(required=True)
    bio = fields.StringField(max_length=500)
    
    # References
    reviews_made = fields.ListField(fields.ReferenceField('Spot'))

class Review(EmbeddedDocument):
    _id = fields.ObjectIdField(required=True, default=lambda: fields.ObjectId())
    stars = fields.IntField(min_value=0, max_value=5)
    comment = fields.StringField(max_length=500)
    user_author = fields.ReferenceField(User, required=True)

class Spot(Document):
    name = fields.StringField(required=True, max_length=50, unique=True)
    breakType = fields.StringField(max_length=30, required=True)
    reviewList = fields.EmbeddedDocumentListField(Review)

# Spot delete rules
# When a Review is deleted -> It gets pulled from the list
Spot.register_delete_rule(Review, "reviewList", PULL)