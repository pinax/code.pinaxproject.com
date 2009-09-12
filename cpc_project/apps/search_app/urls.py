from django.conf.urls.defaults import *
from haystack.views import SearchView
from haystack.forms import HighlightedModelSearchForm

urlpatterns = patterns('haystack.views',
    url(r'^$', SearchView(
        form_class=HighlightedModelSearchForm
    ), name='haystack_search'),
)
