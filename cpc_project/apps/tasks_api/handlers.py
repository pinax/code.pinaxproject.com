from piston.handler import BaseHandler

from tasks.models import Task

class TasksHandler(BaseHandler):
    model = Task
    exclude = ('content_type', 'creator')
    
    def create(self, request):
        task = Task()
        
        task.summary = request.POST.get('summary')
        task.detail = request.POST.get('detail')
        task.creator = request.user
        
        task.save()
        
        return task