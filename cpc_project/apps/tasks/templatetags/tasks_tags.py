from django import template

from django.contrib.contenttypes.models import ContentType

from django.core.urlresolvers import reverse
from django.conf import settings

from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input

from tasks.models import Task

import re

register = template.Library()
task_contenttype = ContentType.objects.get(app_label='tasks', model='task')

@register.inclusion_tag("tasks/task_item.html")
def show_task(task, nudge):
    
    return {
        "nudge": nudge,
        "task": task,
        "MEDIA_URL": settings.MEDIA_URL,
    }

@register.simple_tag
def focus_url(field, value):
    if field is None:
        field = "modified"
    if field == "assignee" and value == None:
        value = "unassigned"
    return reverse("task_focus", args=[field, value])

@register.inclusion_tag("tasks/tag_list.html")
def task_tags(obj):
    taglist = parse_tag_input(obj.tags)
    return {
        "tags": taglist,
    }

class TasksForTagNode(template.Node):
    def __init__(self, tag, var_name):
        self.tag = tag
        self.var_name = var_name

    def render(self, context):
        try:
            tag = template.Variable(self.tag).resolve(context)
        except:
            tag = self.tag
        
        try:
            tasks = Task.objects.filter(id__in=[i[0] for i in TaggedItem.objects.filter(tag__name=str(tag),content_type=task_contenttype).values_list('object_id')])
        except:
            return ''
        
        context[self.var_name] = tasks
        return ''

@register.tag(name='tasks_for_tag')
def tasks_for_tag(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]

    m = re.search(r'(\w+) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name

    tag = m.groups()[0]
    var_name = m.groups()[1]

    return TasksForTagNode(tag, var_name)

@register.filter
def simple_linebreak(text):
    # TODO: replace with better tooltip feature or detail page
    return '<br />'.join(text.splitlines())
    