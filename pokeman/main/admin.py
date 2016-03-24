from django.contrib import admin

from .models import Answer, Post, Vote


admin.site.register(Answer)
admin.site.register(Post)
admin.site.register(Vote)
