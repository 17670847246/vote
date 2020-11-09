"""
将模型注册到Django自带的管理员平台
"""
from django.contrib import admin

# Register your models here.
from polls.models import Subject, Teachers

class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'intro', 'is_hot')
    ordering = ('no', )

class TeachersModelAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'sex', 'birth', 'intro', 'photo', 'good_count', 'bad_count', 'subject')

admin.site.register(Subject, SubjectModelAdmin)
admin.site.register(Teachers, TeachersModelAdmin)