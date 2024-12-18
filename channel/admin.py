from django.contrib import admin
from channel.models import *
# Register your models here.

class MasterCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'category_pic', 'category_pic2','description']
    list_display = ('id','name', 'category_pic', 'category_pic2','description')
    list_per_page = 25

admin.site.register(MasterCategory, MasterCategoryAdmin)

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'category_pic', 'master_category','description',]
    list_display = ('id','name', 'category_pic', 'master_category','description')
    list_per_page = 25

admin.site.register(Category, CategoryAdmin)

class CoursesAdmin(admin.ModelAdmin):
    fields = ['category','name', 'pic', 'data', 'description']
    list_display = ('id','uuid','category','name', 'pic', 'description')
    list_per_page = 25
    read_only_fields = ['uuid']

admin.site.register(Courses, CoursesAdmin)

class CourseQuizAdmin(admin.ModelAdmin):
    fields = ['course', 'index', 'data']
    list_display = ('id','course', 'index')
    list_per_page = 25

admin.site.register(CourseQuiz, CourseQuizAdmin)

admin.site.register(FavoriteCourseContent)
admin.site.register(FavoriteCourse)
admin.site.register(CompleteContent)
admin.site.register(LastCourseContent)