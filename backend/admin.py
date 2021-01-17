from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()

admin.site.register(User, UserAdmin)
admin.site.register(models.Subgroup)
admin.site.register(models.Thread)
admin.site.register(models.Reply)
