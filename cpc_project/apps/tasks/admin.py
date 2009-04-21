from django.contrib import admin
from tasks.models import Task, Release, Iteration

admin.site.register(Task)
admin.site.register(Release)
admin.site.register(Iteration)



