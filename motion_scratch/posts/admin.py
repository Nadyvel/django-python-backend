# Register your models here.
from django.contrib import admin

from posts.models import Post, Comments

admin.site.register(Post)
admin.site.register(Comments)
