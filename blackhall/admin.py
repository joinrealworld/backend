from django.contrib import admin
from .models import BlackhallChat
from django.utils.html import format_html
from django.utils import timezone

@admin.register(BlackhallChat)
class BlackhallChatAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('uuid', 'user', 'formatted_timestamp', 'message_preview')
    
    # Fields to filter by in the admin sidebar
    list_filter = ('user', 'timestamp')
    
    # Fields to search in the admin search bar
    search_fields = ('user__username', 'message')
    
    # Fields that are read-only in the admin detail view
    readonly_fields = ('uuid', 'timestamp')
    
    # Default ordering of entries in the admin list view
    ordering = ('-timestamp',)
    
    # Organize fields into sections in the admin detail view
    fieldsets = (
        (None, {
            'fields': ('uuid', 'user', 'timestamp')
        }),
        ('Message Details', {
            'fields': ('message',)
        }),
    )


    def formatted_timestamp(self, obj):
        """
        Formats the timestamp to a more readable string.
        """
        return timezone.localtime(obj.timestamp).strftime('%Y-%m-%d %H:%M:%S')
    formatted_timestamp.short_description = 'Timestamp'
    formatted_timestamp.admin_order_field = 'timestamp'

    def message_preview(self, obj):
        """
        Provides a concise preview of the message content.
        """
        if isinstance(obj.message, list):
            return f"{len(obj.message)} messages"
        elif isinstance(obj.message, dict):
            msg = obj.message.get('message', '')
            return msg[:50] + ('...' if len(msg) > 50 else '')
        return str(obj.message)[:50]
    message_preview.short_description = 'Message Preview'

    # Optional: Display the full JSON message in a readable format within the detail view
    def get_readonly_fields(self, request, obj=None):
        """
        Makes the message field read-only and displays it in a formatted way.
        """
        if obj:
            return self.readonly_fields + ('formatted_message',)
        return self.readonly_fields

    def formatted_message(self, obj):
        """
        Displays the JSON message in a formatted <pre> block for better readability.
        """
        return format_html('<pre>{}</pre>', obj.message)
    formatted_message.short_description = 'Message'

    # Optionally, override the default display of the message field
    # If you prefer to keep it editable, you can skip this part
    # def message_display(self, obj):
    #     return format_html('<pre>{}</pre>', obj.message)
    # message_display.short_description = 'Message'

