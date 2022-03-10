from django.contrib import admin
from .models import Video, UserVideoJunction


class UserVideoJunctionAdmin(admin.ModelAdmin):
    search_fields = [
        'video__title'
    ]
    list_filter = ('user__username', 'video')


class VideoAdmin(admin.ModelAdmin):
    search_fields = [
        'title'
    ]
    list_display = ('video_id', 'title', 'get_associated_categories')

    def get_associated_categories(self, obj):
        return ', '.join([c.name for c in obj.associated_categories.all()])


admin.site.register(Video, VideoAdmin)
admin.site.register(UserVideoJunction, UserVideoJunctionAdmin)
