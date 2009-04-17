# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.contrib.auth.models import User

from tagging.fields import TagField
from tagging.models import Tag

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
    
def is_assignee(task, user):
    if task.assignee == user:
        return True
    return False

def is_creator(task, user):
    if task.creator == user:
        return True
    return False

def no_assignee(task, user):
    if not task.assignee:
        return True
    return False

def is_assignee_or_none(task, user):
    # current user is assignee or there is no assignee
    if task.assignee == user or not task.assignee:
        return True
    return False
    
def always(task, user):
    return True


STATE_TRANSITIONS = [
    # open
    (1, 1, always, "leave open"),
    (1, 2, is_assignee, "resolved"),
    (1, 4, is_assignee, "in progress"),
    (1, 5, is_assignee_or_none, "discussion needed"),
    (1, 6, is_assignee_or_none, "blocked"),
          
    # resolved
    (2, 1, always, "re-open"),
    (2, 2, always, "leave resolved"),
    (2, 3, is_creator, "close"),
    
    # closed
    (3, 1, always, "re-open"),
    (3, 3, always, "leave closed"),
    
    # in progress
    (4, 4, always, "still in progress"),
    (4, 1, is_assignee, "open"),
    (4, 2, is_assignee, "resolved"),
    (4, 5, is_assignee, "discussion needed"),
    (4, 6, is_assignee, "blocked"),
    
    # discussion needed
    (5, 5, always, "discussion still needed"),
    (5, 1, is_assignee_or_none, "open"),
    (5, 2, is_assignee_or_none, "resolved"),
    (5, 4, is_assignee_or_none, "in progress"),
    (5, 6, is_assignee_or_none, "blocked"),
    
    # blocked
    (6, 6, always, "still blocked"),
    (6, 1, is_assignee_or_none, "open"),
    (6, 2, is_assignee_or_none, "resolved"),
    (6, 4, is_assignee_or_none, "in progress"),
    (6, 5, is_assignee_or_none, "discussion needed"),
]


STATE_CHOICES = (
    ('1', 'open'),
    ('4', 'in progress'), # the assignee is working on it
    ('5', 'discussion needed'), # discussion needed before work can proceed
    ('6', 'blocked'), # blocked on something or someone (other than discussion)
    ('2', 'resolved'), # the assignee thinks it's done
    ('3', 'closed'), # the creator has confirmed it's done
)


RESOLUTION_CHOICES = (
    ('1', 'fixed'),
    ('2', 'duplicate'),
    ('3', 'alreadydone — we have fixed this'),
    ('4', 'irrelevant — another change made this no longer an issue'),
    ('5', 'rejected — current behavior is as intended'),
    ('6', 'nonsense — bad ticket entry'),
    ('7', "worksforme — can't reproduce problem"),
)


REVERSE_STATE_CHOICES = dict((item[1], item[0]) for item in STATE_CHOICES)

STATE_CHOICES_DICT = dict((item[0], item[1]) for item in STATE_CHOICES)
RESOLUTION_CHOICES_DICT = dict((item[0], item[1]) for item in RESOLUTION_CHOICES)


class Task(models.Model):
    """
    a task to be performed.
    """    
    
    STATE_CHOICES = STATE_CHOICES
    RESOLUTION_CHOICES = RESOLUTION_CHOICES
    REVERSE_STATE_CHOICES = REVERSE_STATE_CHOICES
    
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    group = generic.GenericForeignKey("content_type", "object_id")
    
    # @@@ project = models.ForeignKey(Project, related_name="tasks", verbose_name=_('project'))
    
    summary = models.CharField(_('summary'), max_length=100)
    detail = models.TextField(_('detail'), blank=True)
    creator = models.ForeignKey(User, related_name="created_tasks", verbose_name=_('creator'))
    created = models.DateTimeField(_('created'), default=datetime.now)
    modified = models.DateTimeField(_('modified'), default=datetime.now) # task modified when commented on or when various fields changed
    assignee = models.ForeignKey(User, related_name="assigned_tasks", verbose_name=_('assignee'), null=True, blank=True)
    
    tags = TagField()
    
    # status is a short message the assignee can give on their current status
    status = models.CharField(_('status'), max_length=100, blank=True)
    state = models.CharField(_('state'), max_length=1, choices=STATE_CHOICES, default=1)
    resolution = models.CharField(_('resolution'), max_length=2, choices=RESOLUTION_CHOICES, blank=True)
    
    def __unicode__(self):
        return self.summary
    
    def save(self, force_insert=False, force_update=False, comment_instance=None, user=None):
            
        # Do the stock save
        self.modified = datetime.now()
        super(Task, self).save(force_insert, force_update)
        
        # get the task history object
        th = TaskHistory()
        th.task = self
        
        # save the simple fields
        fields = ('summary', 'detail', 'creator', 'created', 'assignee', 'tags', 'status', 'state', 'resolution')
        for field in fields:
            value = getattr(self, field)
            setattr(th, field, value)
              
        if user:
            # If a user is provided then we are editing a record.
            # So the owner of the change is the editor.
            th.owner = user
        else:
            # This record is being created right now, hence the assignment
            # of the creator to the task history object's owner field.
            th.owner = self.creator
        
        # handle the comments
        if comment_instance:
            th.comment = comment_instance.comment

        th.save()
        
    
    def allowable_states(self, user):
        """
        return state choices allowed given current state and user
        """
        
        choices = []
        
        for transition in STATE_TRANSITIONS:
            
            if self.state != str(transition[0]):
                # if the current state does not match a first element in the
                # state transitions we skip to the next transition
                continue
                
            # Fire the validation function.
            if transition[2](self, user): 
                
                # grab the new state and state description
                new_state = str(transition[1]) 
                description = transition[3]
                
                # build new element
                element = (new_state, description) 
                
                # append new element to choices
                choices.append(element) 
                            
        return choices
    
    @models.permalink
    def get_absolute_url(self):
        return ("task_detail", [self.pk])


from threadedcomments.models import ThreadedComment
def new_comment(sender, instance, **kwargs):
    if isinstance(instance.content_object, Task):
        task = instance.content_object
        task.modified = datetime.now()
        
        # pass in the instance.user so that the task history owner is recorded
        # as the commenter
        task.save(comment_instance=instance,user=instance.user)
        group = task.group
        if notification:
            
            if group:
                notify_list = group.member_users.all() # @@@
            else:
                notify_list = User.objects.all()
            
            notification.send(notify_list, "tasks_comment", {
                "user": instance.user, "task": task, "comment": instance, "group": group,
            })
models.signals.post_save.connect(new_comment, sender=ThreadedComment)

class TaskHistory(models.Model):
    STATE_CHOICES = STATE_CHOICES
    RESOLUTION_CHOICES = RESOLUTION_CHOICES
    REVERSE_STATE_CHOICES = REVERSE_STATE_CHOICES
    
    task = models.ForeignKey(Task, related_name="history_task", verbose_name=_('tasks'))
    
    # stock task fields.
    # did not subclass because oddly that did not work. WTF?
    # TODO: fix subclass
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    group = generic.GenericForeignKey("content_type", "object_id")
    summary = models.CharField(_('summary'), max_length=100)
    detail = models.TextField(_('detail'), blank=True)
    creator = models.ForeignKey(User, related_name="history_created_tasks", verbose_name=_('creator'))
    created = models.DateTimeField(_('created'), default=datetime.now)
    modified = models.DateTimeField(_('modified'), default=datetime.now) # task modified when commented on or when various fields changed
    assignee = models.ForeignKey(User, related_name="history_assigned_tasks", verbose_name=_('assignee'), null=True, blank=True)
    
    tags = TagField()
    
    status = models.CharField(_('status'), max_length=100, blank=True)
    state = models.CharField(_('state'), max_length=1, choices=STATE_CHOICES, default=1)
    resolution = models.CharField(_('resolution'), max_length=2, choices=RESOLUTION_CHOICES, default=0, blank=True)
    
    # this stores the comment
    comment = models.TextField(_('comment'), blank=True)
    
    # this stores the owner of this ticket change
    owner = models.ForeignKey(User, related_name="owner", verbose_name=_('Owner'))
    
    def __unicode__(self):
        return 'for ' + str(self.task)
    
    def save(self, force_insert=False, force_update=False):
        self.modified = datetime.now()
        super(TaskHistory, self).save(force_insert, force_update)


class Nudge(models.Model):
    
    nudger = models.ForeignKey(User, related_name="nudger", verbose_name=_('nudger'))
    task = models.ForeignKey(Task, related_name="task", verbose_name=_('task'))
    nudge_date = models.DateTimeField(_('nudge date'), default=datetime.now)