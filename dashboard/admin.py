from django.contrib import admin
from .models import User, Post, Draft, bookappointment

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Draft)
admin.site.register(bookappointment)