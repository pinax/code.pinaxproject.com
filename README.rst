============================
code.pinaxproject.com (CPC)
============================
.. image:: http://slack.pinaxproject.com/badge.svg
   :target: http://slack.pinaxproject.com/

Thisis the site behind code.pinaxproject.com http://code.pinaxproject.com

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates. 
This collection can be found at http://pinaxproject.com.

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a code of conduct, which can be found here  http://pinaxproject.com/pinax/code_of_conduct/.

The Pinax documentation is available at http://pinaxproject.com/pinax/.

For updates and news regarding the Pinax Project, please follow us on Twitter at @pinaxproject and check out our blog http://blog.pinaxproject.com.

Installation
=============

For development purposes. cd to cpc_project root::

    pip install --requirement requirements.txt
    python manage.py syncdb
    python manage.py reindex
    python manage.py runserver    
