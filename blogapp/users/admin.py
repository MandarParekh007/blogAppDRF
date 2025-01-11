from django.contrib import admin
from .models import CustomUser
from blogs.models import Blogs

# Register your models here.
admin.site.register(Blogs)