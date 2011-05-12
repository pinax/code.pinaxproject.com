from django import forms

from bulk_actions import handlers


class BulkActionForm(forms.Form):
    
    action = forms.ChoiceField(choices=[])
    objects = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, *args, **kwargs):
        super(BulkActionForm, self).__init__(*args, **kwargs)
        self.fields["action"].choices = [(x[0], x[1].verbose_name) for x in handlers]
        
    def clean_action(self):
        action = int(self.cleaned_data["action"])
        for handler in handlers:
            if action == handler[0]:
                return handler[1]


class BulkActionInputFormBase(forms.Form):
    
    objects = forms.MultipleChoiceField(widget=forms.MultipleHiddenInput)
