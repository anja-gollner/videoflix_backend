from django.contrib import admin
from video_app.models import UserVideoProgress, Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'video_file',
                    'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description', 'category')
    ordering = ('-created_at',)


admin.site.register(Video, VideoAdmin)

admin.site.register(UserVideoProgress)
