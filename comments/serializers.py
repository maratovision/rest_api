from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializerHard(serializers.Serializer):
    text = serializers.CharField(max_length=50, required=True, min_length=1)
