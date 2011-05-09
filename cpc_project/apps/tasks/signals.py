import django.dispatch


task_created = django.dispatch.Signal(
    providing_args=[
        "user", "task", "group"
    ]
)
task_nudged = django.dispatch.Signal(
    providing_args=[
        "nudger", "task", "count"
    ]
)
task_status_changed = django.dispatch.Signal(
    providing_args=[
        "user", "task", "group"
    ]
)
task_changed = django.dispatch.Signal(
    providing_args=[
        "user", "task", "group"
    ]
)
task_assignment_changed = django.dispatch.Signal(
    providing_args=[
        "user", "task", "group"
    ]
)
task_tags_changed = django.dispatch.Signal(
    providing_args=[
        "user", "task", "group"
    ]
)