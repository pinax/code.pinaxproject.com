from django import forms
from django.db.models import get_model
from django.utils import simplejson
from django.utils.safestring import mark_safe
from tagging.models import Tag

class TagAutoCompleteInput(forms.TextInput):
    class Media:
        css = {
            'all': ('css/jquery.autocomplete.css',)
        }
        js = (
            'jquery-1.3.min.js',
            'js/jquery.bgiframe.min.js',
            'js/jquery.ajaxQueue.js',
            'js/jquery.autocomplete.min.js'
        )
    def __init__(self, app_label, model, *args, **kwargs):
        self.model = get_model(app_label, model)
        super(TagAutoCompleteInput, self).__init__(*args, **kwargs)
        
    def render(self, name, value, attrs=None):
        output = super(TagAutoCompleteInput, self).render(name, value, attrs)
        page_tags = Tag.objects.usage_for_model(self.model)
        tag_list = simplejson.dumps([tag.name for tag in page_tags], ensure_ascii=False)
        
        return output + mark_safe(u'''<script type="text/javascript">
            jQuery("#id_%s").autocomplete(%s, {
                max: 10,
                highlight: false,
                multiple: true,
                multipleSeparator: " ",
                scroll: true,
                scrollHeight: 300,
                matchContains: true,
                autoFill: true,
            });
            </script>''' % (name, tag_list))