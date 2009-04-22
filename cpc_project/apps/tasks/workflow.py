# -*- coding: utf-8 -*-

"""
We break out workflow elements to enable us to more easily refactor in the
future.
"""

from django.contrib.auth.models import Group

TASK_MANAGER = 'coredev'

def is_task_manager(task, user):
    if Group.objects.filter(name__exact=TASK_MANAGER).filter(user=user):
        return True
    return False

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