from django.contrib import admin
from .models import Video, UserVideoJunction


class UserVideoJunctionAdmin(admin.ModelAdmin):
    search_fields = [
        'video__title'
    ]
    list_filter = ('user__username', 'video')


admin.site.register(Video)
admin.site.register(UserVideoJunction, UserVideoJunctionAdmin)
