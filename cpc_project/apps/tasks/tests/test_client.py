# coding: utf-8

from django.test import TestCase
from django.test.client import Client


class TestAddForm(TestCase):
    
    def setUp(self):
        # Every test needs a client
        self.client = Client()
    
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
         
         
         