from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from .models import Comment

# Create your views here.
def index(request):
    template = loader.get_template('application/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

# Get specific comment
def get(request, comment_id):
    comments = Comment.objects
    try: 
        comment = comments.get(pk=comment_id)
    except Comment.DoesNotExist:
        raise Http404("Comment with ID (" + str(comment_id) + ") does not exist")
    return HttpResponse(comments.get(pk=comment_id))

# Get all comments possible (Too many then possible slice them)
def comments(request):
    comments = Comment.objects.all()
    output = dict()
    for c in comments:
        output[c.id] = c.comment_text
    return HttpResponse(str(output))
