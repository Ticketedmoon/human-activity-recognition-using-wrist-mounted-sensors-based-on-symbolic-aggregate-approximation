from django.shortcuts import render
from django.http import HttpResponse

from .models import Comment

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the application index.")

def get(request, comment_id):
    comments = Comment.objects
    return HttpResponse(comments.get(pk=comment_id))

def getAllComments(request):
    comments = Comment.objects.all()
    output = dict()
    for c in comments:
        output[c.id] = c.comment_text
    return HttpResponse(str(output))
