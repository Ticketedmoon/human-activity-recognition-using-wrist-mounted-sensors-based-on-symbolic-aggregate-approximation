from django.urls import path

from . import views

urlpatterns = [
    # Default Path
    path('', views.index, name='index'),

    # Blog Path
    path('blog/', views.blog, name='blog'),
    
    # Research Path
    path('research/', views.research, name='research'),

    # Discussion Path
    path('discussion/', views.discussion, name='discussion'),

    # Comment Results Path
    path('comments/<int:comment_id>/', views.get, name="get"),

    # Get all comments
    path('comments/', views.comments, name="comments")
]