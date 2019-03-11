from django.db import models

# Create your models here.
class Comment(models.Model):
    comment_id = models.BigIntegerField(primary_key=True)
    comment_text = models.CharField(max_length=200)
    comment_author = models.CharField(max_length=30, null=True)
    comment_publish_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.comment_text
    
    # Table name
    class Meta:
        db_table = 'application_comments'