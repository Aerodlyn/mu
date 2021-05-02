from django.contrib import admin

from .models import (
    Comment,
    Community,
    Membership,
    Post
)

admin.site.register (Comment)
admin.site.register (Community)
admin.site.register (Membership)
admin.site.register (Post)
