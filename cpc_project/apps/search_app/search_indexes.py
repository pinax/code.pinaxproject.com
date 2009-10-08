import datetime
from haystack import indexes, site
from tasks.models import Task
from wiki.models import Article

class TaskModelIndex(indexes.ModelSearchIndex):
    rendered = indexes.CharField(use_template=True, indexed=False)

    class Meta:
        fields = ['created', 'summary', 'detail']

class ArticleModelIndex(indexes.ModelSearchIndex):
    rendered = indexes.CharField(use_template=True, indexed=False)

    class Meta:
        fields = ['title', 'summary', 'content']

site.register(Task, TaskModelIndex)
site.register(Article, ArticleModelIndex)
