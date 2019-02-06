from django.urls import path

from . import views

urlpatterns = [
    # Default Path
    path('', views.index, name='index'),
    
    # Comment Results Path
    path('comments/<int:comment_id>/', views.get, name="get"),

    # Get all comments
    path('comments/all/', views.getAllComments, name="getAllComments")
]