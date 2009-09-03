import datetime
from haystack import indexes, site
from tasks.models import Task

class TaskModelIndex(indexes.ModelSearchIndex):
    rendered = indexes.CharField(use_template=True, indexed=False)

    class Meta:
        fields = ['created', 'summary', 'detail']

site.register(Task, TaskModelIndex)
