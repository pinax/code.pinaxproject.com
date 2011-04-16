from django.contrib import admin

from tasks.models import Task, PinnedList


admin.site.register(Task)
admin.site.register(PinnedList)