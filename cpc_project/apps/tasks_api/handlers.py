from piston.handler import BaseHandler

from tasks.models import Task

class TasksHandler(BaseHandler):
    model = Task
    exclude = ('content_type', 'creator')
    
    def read(self, request, task_id=None):
        if task_id:
            task = Task.objects.get(pk=task_id)
            return task
        else:
            return Task.objects.all()
    
    def create(self, request):
        task = Task()
        
        task.summary = request.POST.get('summary')
        task.detail = request.POST.get('detail')
        task.creator = request.user
        
        task.save()
        
        return task