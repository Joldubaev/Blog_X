from django.contrib import admin

from django.contrib import admin

from main.models import *

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Favorites)