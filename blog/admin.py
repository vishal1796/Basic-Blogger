from django.contrib import admin
from blog.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ["title","timestamp","updated"]
    list_display_link = ["title"]
    list_filter = ["updated"]
    search_fields = ["title"]

    class Meta:        ##### research meta #####
        model = Post

admin.site.register(Post,PostAdmin)