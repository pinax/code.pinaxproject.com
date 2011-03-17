from django.contrib.auth.models import User

from notification import models as notification

from tasks import signals


def signal(signals, sender=None):
    def _wrapped(func):
        if not hasattr(signals, "__iter__"):
            _s = [signals]
        else:
            _s = signals
        for s in _s:
            s.connect(func, sender=sender)
        return func
    return _wrapped


def task_notify_list(kwargs):
    if kwargs["group"]:
        users = kwargs["group"].member_queryset()
    else:
        users = User.objects.all()
    return users.exclude(id__exact=kwargs["user"].id)


@signal([signals.task_created])
def task_created(sender, **kwargs):
    # @@@ temporarily turned off
    return
    notification.send(task_notify_list(dict(kwargs, user=kwargs["creator"])), "tasks_new", {
        "creator": kwargs["creator"],
        "task": kwargs["task"],
        "group": kwargs["group"]
    })


@signal([signals.task_nudged])
def task_nudged(sender, **kwargs):
    # @@@ temporarily turned off
    return
    notification.send([kwargs["task"].assignee], "tasks_nudge", {
        "nudger": kwargs["nudger"],
        "task": kwargs["task"],
        "count": kwargs["count"],
    })

@signal([signals.task_status_changed])
def task_status_changed(sender, **kwargs):
    # @@@ temporarily turned off
    return
    notification.send(task_notify_list(kwargs), "tasks_status", {
        "user": kwargs["user"],
        "task": kwargs["task"],
        "group": kwargs["group"]
    })


@signal([signals.task_changed])
def task_changed(sender, **kwargs):
    # @@@ temporarily turned off
    return
    notification.send(task_notify_list(kwargs), "tasks_change", {
        "user": kwargs["user"],
        "task": kwargs["task"],
        "group": kwargs["group"],
        "new_state": kwargs["task"].get_state_display()
    })


@signal([signals.task_assignment_changed])
def task_assignment_changed(sender, **kwargs):
    # @@@ temporarily turned off
    return
    notification.send(task_notify_list(kwargs), "tasks_assignment", {
        "user": kwargs["user"],
        "task": kwargs["task"],
        "assignee": kwargs["task"].assignee,
        "group": kwargs["group"],
    })


@signal([signals.task_tags_changed])
def task_tags_changed(sender, **kwargs):
    # @@@ temporarily turned off
    return
    notification.send(task_notify_list(kwargs), "tasks_tags", {
        "user": kwargs["user"],
        "task": kwargs["task"],
        "group": kwargs["group"],
    })
