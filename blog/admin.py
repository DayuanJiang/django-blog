from django.contrib import admin
from .models import Post, Tag
from mptt.admin import DraggableMPTTAdmin
# Register your models here.


admin.site.register(Post)
#admin.site.register(Category, DraggableMPTTAdmin)
admin.site.register(Tag)