from rest_framework import serializers
from .models import Complaint, Tag


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RestrictedComplaintSerializer(serializers.ModelSerializer):
    complainant = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    tag = serializers.CharField(required=False)

    class Meta:
        model = Complaint
        fields = ('id', 'complainant', 'title', 'description', 'tag')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ('id', 'comment')
