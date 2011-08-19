from django.db.models import get_models, signals
from django.utils.translation import ugettext_noop as _

from notification.models import NoticeType


def create_notice_types(app, created_models, verbosity, **kwargs):
    NoticeType.create(
        label = "tasks_new",
        display = _("New Task"),
        description = _("a new task been created"),
        default = 2
    )
    NoticeType.create(
        label = "tasks_comment",
        display = _("Task Comment"),
        description = _("a new comment has been made on a task"),
        default = 2
    )
    NoticeType.create(
        label = "tasks_change",
        display = _("Task State Change"),
        description = _("there has been a change in the state of a task"),
        default = 2
    )
    NoticeType.create(
        label = "tasks_assignment",
        display = _("Task Assignment"),
        description = _("a task has been (re)assigned"),
        default = 2
    )
    NoticeType.create(
        label = "tasks_status",
        display = _("Task Status Update"),
        description = _("there has been a status update to a task"),
        default = 2
    )
    NoticeType.create(
        label = "tasks_tags",
        display = _("Task Tag Update"),
        description = _("there has been a change in the tagging of a task"),
        default = 2
    )
    NoticeType.create(
        label = "tasks_nudge",
        display = _("Task Nudge"),
        description = _("there has been a nudge of a task"),
        default = 2
    )
import notification.models
signals.post_syncdb.connect(create_notice_types, sender=notification.models)
