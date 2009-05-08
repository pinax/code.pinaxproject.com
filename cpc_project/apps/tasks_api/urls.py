from django.conf.urls.defaults import *

from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from tasks_api.handlers import TasksHandler

auth = HttpBasicAuthentication(realm="Pinax realm")

tasks_resource = Resource(TasksHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^tasks/$', tasks_resource),
)