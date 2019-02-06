from django.db import models

# Create your models here.
class Comment(models.Model):
    comment_text = models.CharField(max_length=200)
    publish_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.comment_text