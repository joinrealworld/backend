from django.contrib import admin
from polls.models import *

# Register your models here.
class MasterPollQuetionAdmin(admin.ModelAdmin):
    fields = ['quetion', 'master_category']
    list_display = ('id', 'quetion', 'master_category','created_at')
    list_per_page = 25

admin.site.register(MasterPollQuetion, MasterPollQuetionAdmin)

class MasterPollOptionAdmin(admin.ModelAdmin):
    fields = ['option', 'poll_quetion']
    list_display = ('id', 'option', 'poll_quetion', 'created_at')
    list_per_page = 25

admin.site.register(MasterPollOption, MasterPollOptionAdmin)

class UserPollAdmin(admin.ModelAdmin):
    fields = ['selected_option', 'is_checked', 'poll_quetion','user']
    list_display = ('id', 'selected_option', 'is_checked', 'poll_quetion','user', 'created_at')
    list_per_page = 25

admin.site.register(UserPoll, UserPollAdmin)