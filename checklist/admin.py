from django.contrib import admin
from checklist.models import *

# Register your models here.
class MasterCheckListAdmin(admin.ModelAdmin):
    fields = ['checklist', 'options']
    list_display = ('id','uuid','checklist','options','created_at')
    list_per_page = 25

admin.site.register(MasterCheckList, MasterCheckListAdmin)


class UserDailyCheckListAdmin(admin.ModelAdmin):
    fields = ['master_checklist']
    list_display = ('id','uuid', 'master_checklist','created_at')
    list_per_page = 25

admin.site.register(UserDailyCheckList, UserDailyCheckListAdmin)

class DailyCheckedAdmin(admin.ModelAdmin):
    fields = ['user', 'data']
    list_display = ('id','uuid', 'user', 'data', 'created_at')
    list_per_page = 25

admin.site.register(DailyChecked, DailyCheckedAdmin)