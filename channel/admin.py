from django.contrib import admin
from channel.models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'category_pic', 'description']
    list_display = ('id','name', 'category_pic', 'description')
    list_per_page = 25

admin.site.register(Category, CategoryAdmin)

class CoursesAdmin(admin.ModelAdmin):
    fields = ['category', 'name', 'data']
    list_display = ('id','category', 'name',)
    list_per_page = 25

admin.site.register(Courses, CoursesAdmin)

class CourseQuizAdmin(admin.ModelAdmin):
    fields = ['course', 'index', 'data']
    list_display = ('id','course', 'index')
    list_per_page = 25

admin.site.register(CourseQuiz, CourseQuizAdmin)