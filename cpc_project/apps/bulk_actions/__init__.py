from bulk_actions.actions import BulkActionBase


handlers = set()


def register(klass):
    if not issubclass(klass, BulkActionBase):
        raise Exception("Bulk actions must derive from BulkActionBase")
    handlers.add((len(handlers), klass))
