from django.shortcuts import render
from django.http import HttpResponse

from .models import Comment

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the application index.")

# Get specific comment
def get(request, comment_id):
    comments = Comment.objects
    return HttpResponse(comments.get(pk=comment_id))

# Get all comments possible (Too many then possible slice them)
def comments(request):
    comments = Comment.objects.all()
    output = dict()
    for c in comments:
        output[c.id] = c.comment_text
    return HttpResponse(str(output))
