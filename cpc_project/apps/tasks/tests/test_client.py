# coding: utf-8

from django.test import TestCase


rst_markup = """
Sample Header
===============

Blah blah blah

Lower Header
-------------

Blah blah blah
"""

class TestAddForm(TestCase):
    fixtures = ['test_tasks.json']    
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_add_buttons(self):
        response = self.client.get('/tasks/add/')

        # Check that the response is 200 OK.
        self.failUnlessEqual(response.status_code, 200)

        # check that there is an add button
        self.assertContains(response, '<input type="submit" value="Add task"/>')

        # check that there is an add another task button
        self.assertContains(response, 'add-another-task')
         
    def test_markup(self):

        # log in so the user has task add rights.
        self.client.login(username='admin', password='test')        
        
        # create some sample form data
        form_data = {'summary': 'my simple test', 
                'detail': rst_markup,
                'markup':'rst',
                'assignee':'',
                'tags':''
                }
                
        # post the form
        response = self.client.post('/tasks/add/', form_data)
        
        response = self.client.get('/tasks/task/3/')
        
        self.assertContains(response, '<h1 class="title">Sample Header</h1>')