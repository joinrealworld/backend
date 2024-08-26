from django.contrib import admin
from media_channel.models import *

# Register your models here.
class MediaChannelAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'content', 'timestamp')
    list_display_links = ('uuid', 'user')
    search_fields = ('user__username', 'message', 'content__id')
    list_filter = ('user', 'timestamp')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
admin.site.register(MediaChannel, MediaChannelAdmin)


class MediaChannelLikeAdmin(admin.ModelAdmin):
    list_display = ('media_channel', 'user', 'timestamp')
    list_display_links = ('media_channel', 'user')
    search_fields = ('media_channel__uuid', 'user__username')
    list_filter = ('user', 'timestamp')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
admin.site.register(MediaChannelLike, MediaChannelLikeAdmin)
