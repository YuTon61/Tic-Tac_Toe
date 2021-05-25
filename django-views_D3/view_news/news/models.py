from django.db import models

# Create your models here.
###
class News(models.Model):
    datetime   = models.DateTimeField(auto_now_add = True)
    title      = models.CharField(max_length = 255)
    text       = models.TextField()
	
    def __str__(self):
        return f'{self.title}: {self.text[:20]}'
		
