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
    
def no_assignee(task, user):
    if not task.assignee:
        return True
    return False
    
def other_than_assignee(task, user):
    if task.assignee != user:
        return True
    return False

STATE_TRANSITIONS = [
    # open
    (1, 1, is_assignee, "Open"),
    (1, 4, is_assignee, "In Progress"),
    (1, 5, is_assignee, "Discussion Needed"),
    (1, 6, is_assignee, "Block"),
    (1, 2, is_assignee, "Resolve"),
    (1, 1, no_assignee, "Open"),
    (1, 5, no_assignee, "Discussion Needed"),
    (1, 6, no_assignee, "Block"),
    (1, 1, other_than_assignee, "Open"),
          
    # resolved
    (2, 2, is_assignee, "Resolved"),
    (2, 1, is_assignee, "Reopen"),
    (2, 3, is_assignee, "Close"),
    (2, 2, no_assignee, "Resolved"),
    (2, 1, no_assignee, "Reopen"),
    (2, 2, other_than_assignee, "Resolved"),
    (2, 1, other_than_assignee, "Reopen"),
    
    # closed
    (3, 3, is_assignee, "Closed"),
    (3, 1, is_assignee, "Reopen"),
    (3, 3, no_assignee, "Closed"),
    (3, 1, no_assignee, "Reopen"),
    (3, 3, other_than_assignee, "Closed"),
    (3, 1, other_than_assignee, "Reopen"),
    
    # in progress
    (4, 4, is_assignee, "In progress"),
    (4, 1, is_assignee, "Move to open"),
    (4, 5, is_assignee, "Discussion needed"),
    (4, 6, is_assignee, "Block"),
    (4, 2, is_assignee, "Resolve"),
    (4, 4, no_assignee, "In progress"),
    (4, 4, other_than_assignee, "In progress"),
    
    # discussion needed
    (5, 5, is_assignee, "Discussion Needed"),
    (5, 1, is_assignee, "Reopen"),
    (5, 4, is_assignee, "In Progress"),
    (5, 6, is_assignee, "Block"),
    (5, 2, is_assignee, "Resolved"),
    (5, 5, no_assignee, "Discussion Needed"),
    (5, 1, no_assignee, "Reopen"),
    (5, 4, no_assignee, "In Progress"),
    (5, 6, no_assignee, "Block"),
    (5, 2, no_assignee, "Resolved"),
    (5, 5, other_than_assignee, "Discussion Needed"),
    
    # blocked
    (6, 6, is_assignee, "Block"),
    (6, 1, is_assignee, "Reopen"),
    (6, 5, is_assignee, "Discussion Needed"),
    (6, 4, is_assignee, "In Progress"),
    (6, 2, is_assignee, "Resolve"),
    (6, 6, no_assignee, "Block"),
    (6, 1, no_assignee, "Reopen"),
    (6, 5, no_assignee, "Discussion Needed"),
    (6, 4, no_assignee, "In Progress"),
    (6, 2, no_assignee, "Resolve"),
    (6, 6, other_than_assignee, "Block"),
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
    ('0', 'Not yet resolved'),
    ('1', 'Fixed'),
    ('2', 'Duplicate'),
    ('3', 'Already done - We have fixed this'),
    ('4', 'No longer relevant - Done in a previous release'),
    ('5', "Wontfix - Bugs we aren't going to fix"),
    ('6', 'Invalid - bad ticket entry')
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
    resolution = models.CharField(_('resolution'), max_length=2, choices=RESOLUTION_CHOICES, default=0, blank=True)
    
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
            
        # TODO: fix responsible party   
        #if user:
        #    th.responsible_party = user
        #else:
        #    th.responsible_party = self.creator
        
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
        #task.save(comment_instance=instance,user=comment_instance.user)
        task.save(comment_instance=instance)
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
    
    # this stores the responsible party.
    # TODO: work on this for CPC ticket #131
    # responsible_party = models.ForeignKey(User, related_name="responsible_party", verbose_name=_('Responsible Party'))
    
    def __unicode__(self):
        return 'for ' + str(self.task)
    
    def save(self, force_insert=False, force_update=False):
        self.modified = datetime.now()
        super(TaskHistory, self).save(force_insert, force_update)


class Nudge(models.Model):
    
    nudger = models.ForeignKey(User, related_name="nudger", verbose_name=_('nudger'))
    nudged = models.ForeignKey(User, related_name="nudged", verbose_name=_('nudged'))
