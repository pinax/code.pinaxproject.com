from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

import bulk_actions

from bulk_actions import actions
from bulk_actions.forms import BulkActionInputFormBase

from taggit.forms import TagField

from tasks.models import Task


class SetTagsForm(BulkActionInputFormBase):
    
    tags = TagField()


class SetTags(actions.BulkActionBase):
    
    verbose_name = "Set Tags"
    form = SetTagsForm
    process_url_name = "bulk_actions_set_tags"
    
    @staticmethod
    def show_form(request, objects, **kwargs):
        f = SetTags.form(initial={"objects": [o.pk for o in objects]})
        return render_to_response("bulk_actions/set_tags.html", RequestContext(request, {
            "form": f,
            "process_url": reverse(SetTags.process_url_name)
        }))
    
    @staticmethod
    def process_form(request, **kwargs):
        f = SetTags.form(request.POST)
        f.fields["objects"].choices = [(o.pk, o.summary) for o in Task.objects.all()]
        if f.is_valid():
            for task_pk in f.cleaned_data["objects"]:
                task = Task.objects.get(pk=task_pk)
                for tag in f.cleaned_data["tags"]:
                    task.tags.add(tag)
                task.save()
            return redirect(reverse("task_list") + "?" + request.META["QUERY_STRING"])
        
        return render_to_response("bulk_actions/set_tags.html", RequestContext(request, {
            "form": f,
            "process_url": reverse(SetTags.process_url_name)
        }))


bulk_actions.register(SetTags)
