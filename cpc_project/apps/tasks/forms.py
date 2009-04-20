from datetime import datetime

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_app
from django.contrib.auth.models import User

from tasks.models import Task, TaskHistory


class TaskForm(forms.ModelForm):
    def __init__(self, group, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # @@@ for now this following filtering is commented out until we work out how to do generic membership
        self.fields["assignee"].queryset = self.fields["assignee"].queryset.order_by('username')
        self.fields['summary'].widget.attrs["size"] = 65
        
    def save(self, commit=True):

        return super(TaskForm, self).save(commit)        
    
    class Meta:
        model = Task
        fields = ('summary', 'detail', 'assignee', 'tags')


class EditTaskForm(forms.ModelForm):
    """
    a form for editing task
    """
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EditTaskForm, self).__init__(*args, **kwargs)
        self.fields["assignee"].queryset = self.fields["assignee"].queryset.order_by('username')        
        
        self.fields.keyOrder = ["summary","tags", "status", "assignee", "state", "resolution"]
        
        if self.instance.assignee != user:
            del self.fields["status"]
            
        
        # @@@ for now this following filtering is commented out until we work out how to do generic membership
        # self.fields["assignee"].queryset = self.fields["assignee"].queryset.filter(project=project)
        
        self.fields["state"].choices = self.instance.allowable_states(user)

    # TODO: work on this for CPC ticket #131
    def save(self, commit=False):
        
        # we manually save to the Task object so we can ensure that the user
        # is passed to the custom Task save method
        if commit:
            task = Task.objects.get(pk__exact=self.instance.pk)
            for field in self.fields.keyOrder:
                value = getattr(self.instance, field)
                setattr(task, field, value)    
            task.save(user = self.user)            
        
        return super(EditTaskForm, self).save(True) 
            
        
        
    status = forms.CharField(required=False, widget=forms.TextInput(attrs={'size':'50', 'maxlength': '100'}))
    
    class Meta(TaskForm.Meta):     
        fields = ('summary','status', 'assignee', 'state', 'tags', 'resolution')
