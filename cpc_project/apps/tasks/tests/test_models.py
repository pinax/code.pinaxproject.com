# coding: utf-8

from django.contrib.auth.models import User
from django.test import TestCase

from tasks.models import Task, TaskHistory

class TestTask(TestCase):
    fixtures = ['test_tasks.json']
    
    def setUp(self):
        self.task = Task.objects.get(pk__exact=1)
        self.user_admin = User.objects.get(username__exact='admin')
        self.user_joe = User.objects.get(username__exact='joe')
    
    def tearDown(self):
        pass
    
    def test_allowable_states(self):
        """Doing some simple assertions based off states"""
        
        # Task is just created
        states = self.task.allowable_states(self.user_admin)
        self.assertEquals(states,
            [('1', 'leave open'), ('5', 'discussion needed'), ('6', 'blocked')])
        
        # Now we assign it. This is what the new user sees
        self.task.assignee = self.user_joe
        self.task.save(user=self.user_admin)
        states = self.task.allowable_states(self.user_joe)
        self.assertEquals(states,
            [('1', 'leave open'), ('2', 'resolved'), ('4', 'in progress'),
            ('5', 'discussion needed'), ('6', 'blocked')])
        
        # this is what the creator sees
        states = self.task.allowable_states(self.user_admin)
        self.assertEquals(states, [('1', 'leave open')])
        
        # Task is now moved to in-progress. this is what the assignee can see.
        self.task.state = "4"
        self.task.save(user=self.user_joe)
        states = self.task.allowable_states(self.user_joe)
        self.assertEquals(states,
            [('4', 'still in progress'), ('1', 'open'), ('2', 'resolved'),
            ('5', 'discussion needed'), ('6', 'blocked')])
        
class TestTaskHistory(TestCase):
    fixtures = ['test_tasks.json']
        
    def setUp(self):
        self.task = Task.objects.get(pk__exact=1)
        self.user_admin = User.objects.get(username__exact='admin')
        self.user_joe = User.objects.get(username__exact='joe')
    
    def tearDown(self):
        pass        
        
    def test_history(self):
        """ lets see if history tracks user changes if done against the task"""
        
        # we have admin assign joe to the task.
        self.task.assignee = self.user_joe
        self.task.save(user=self.user_admin)
        
        # fetch the history
        history = self.task.history_task.all()[0]
        
        # The task assignee should be joe
        self.assertEquals(history.assignee, self.user_joe)
        
        # the person who made the change was admin
        self.assertEquals(history.owner, self.user_admin)        
