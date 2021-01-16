from django.db import models

class Subgroup(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
