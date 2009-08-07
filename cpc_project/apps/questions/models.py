from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class Question(models.Model):
    
    object_id = models.IntegerField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    group = generic.GenericForeignKey()
    
    question = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, related_name="questions")
    created = models.DateTimeField(default=datetime.now)
    
    def get_absolute_url(self, group=None):
        kwargs = {
            "question_id": self.pk,
        }
        if group:
            return group.content_bridge.reverse("questions_question_detail", kwargs=kwargs)
        return reverse("questions_question_detail", kwargs=kwargs)


class Response(models.Model):
    
    question = models.ForeignKey(Question)
    content = models.TextField()
    user = models.ForeignKey(User, related_name="responses")
    created = models.DateTimeField(default=datetime.now)
    
    def get_absolute_url(self, group=None):
        return "%s#%d" % (self.question.get_absolute_url(group), self.pk)

