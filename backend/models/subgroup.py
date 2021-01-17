from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Subgroup(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='child_group', null=True, blank=True)
    members = models.ManyToManyField(User, related_name='subgroups', blank=True)
