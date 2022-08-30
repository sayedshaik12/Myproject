from django.db import models
from datetime import datetime
# Create your models here.

class Datasave(models.Model):
    full_name=models.CharField(max_length=50)
    mobile_number=models.IntegerField()
    email=models.EmailField(max_length=40,default='liveforothers@gmail.com')
    def __str__(self):
        return self.full_name
class Blogpost(models.Model):
    heading=models.CharField(max_length=100)
    topic=models.CharField(max_length=100,default='any topic')
    description=models.CharField(max_length=100000)
    created_time=models.DateTimeField(default=datetime.now,blank=True)
    def __str__(self):
        return self.heading

    
