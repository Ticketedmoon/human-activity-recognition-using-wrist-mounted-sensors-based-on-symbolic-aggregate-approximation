from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import render_to_response
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime

from .models import Comment

# Homepage.
def index(request):
    template = loader.get_template('application/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

# Blog.
def blog(request):
    template = loader.get_template('application/blog.html')
    context = {}
    return HttpResponse(template.render(context, request))

# Research.
def research(request):
    template = loader.get_template('application/research.html')
    context = {}
    return HttpResponse(template.render(context, request))

# Discussion.
def discussion(request):
    template = loader.get_template('application/discussion.html')
    context = {
        'comments': Comment.objects.all()
    }
    return HttpResponse(template.render(context, request))

# Get all comments possible (Too many then possible slice them)
def comments(request):
    comments = Comment.objects.all()
    return HttpResponse({'comments': comments})

# Get specific comment
def get(request, comment_id):
    comments = Comment.objects
    try: 
        comment = comments.get(pk=comment_id)
    except Comment.DoesNotExist:
        raise Http404("Comment with ID (" + str(comment_id) + ") does not exist")
    return HttpResponse(comments.get(pk=comment_id))

def validate_comment(request):
    unique_id = Comment.objects.count() + 1
    date_modified = datetime.now()
    author = request.GET.get('username', None)
    desc = request.GET.get('comment_description', None)
    new_entry = Comment(comment_id=unique_id, comment_author=author, comment_text=desc, comment_publish_date=date_modified)
    new_entry.save()
    return JsonResponse((author, desc), safe=False)