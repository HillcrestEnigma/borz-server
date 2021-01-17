from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Thread(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='threads_authored', null=True, blank=True)
    subgroup = models.ForeignKey('Subgroup', on_delete=models.SET_NULL, related_name='threads', null=True, blank=True)

class Reply(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='replies_authored', null=True, blank=True)
    thread = models.ForeignKey(Thread, related_name='replies', on_delete=models.CASCADE)
