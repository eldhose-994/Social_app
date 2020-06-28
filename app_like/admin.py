from django.contrib import admin

from app_like.models import Post, PostImages, Reaction, Tag, TagWeight

# Register your models here.

admin.site.register(Post)
admin.site.register(PostImages)
admin.site.register(Reaction)
admin.site.register(Tag)
admin.site.register(TagWeight)
