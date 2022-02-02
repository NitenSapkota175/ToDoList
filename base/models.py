from asyncio import Task
from email.policy import default
from django.db import models
from tables import Description
from django.contrib.auth.models import User
# Create your models here.
#models are class respresent dtabase table

class Task(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,null=True,blank=True) #here we are doing cascade is because if the user is deleted then we want to delete all the task they have ceated and if you dont want to dont want to do that the you can just do models.SET_NULL this means if the user is deleted it wont delete that task , thi sis many to one relationship
    title = models.CharField(max_length=200)  
    description = models.TextField(null=True,blank=True)
    complete =  models.BooleanField(default=False)
    created =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']