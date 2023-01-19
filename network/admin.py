from django.contrib import admin
from .models import User, Post

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("following", "followers")

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
