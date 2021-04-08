from django.shortcuts import render
from rest_framework.response import Response

from .serializers import *
from rest_framework import views, status
from .models import *

class CommentView(views.APIView):

    def get(self, request, *args, **kwargs):
        comment = Comment.objects.all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)


class CommentDetailView(views.APIView):

    def get(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=kwargs['comment_id'])
        except Comment.DoesNotExist:
            return Response({'data': 'Comment not found'}, status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
