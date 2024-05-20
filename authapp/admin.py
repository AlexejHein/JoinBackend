from django.contrib import admin
from .models import Contact, Subtask, Task


class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1


class TaskAdmin(admin.ModelAdmin):
    inlines = [SubtaskInline]


admin.site.register(Task, TaskAdmin)
admin.site.register(Contact)
