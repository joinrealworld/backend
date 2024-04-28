from django.contrib import admin
from checklist.models import *

# Register your models here.
class MasterCheckListAdmin(admin.ModelAdmin):
    fields = ['data']
    list_display = ('id','uuid','data','created_at')
    list_per_page = 25

admin.site.register(MasterCheckList, MasterCheckListAdmin)


class UserDailyCheckListAdmin(admin.ModelAdmin):
    fields = ['user','selected']
    list_display = ('id','uuid', 'user','selected','created_at')
    list_per_page = 25

admin.site.register(UserDailyCheckList, UserDailyCheckListAdmin)