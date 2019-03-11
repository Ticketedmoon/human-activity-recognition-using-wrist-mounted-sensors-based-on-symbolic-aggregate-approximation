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

    # Get all comments
    path('comments/', views.comments, name="comments"),

    # Comment Results Path
    path('comments/<int:comment_id>/', views.get, name="get"),

    # comment add
    path('comments/validate_comment/', views.validate_comment, name='validate_comment'),

]