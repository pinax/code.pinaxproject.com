============================
code.pinaxproject.com (CPC)
============================
.. image:: http://slack.pinaxproject.com/badge.svg
   :target: http://slack.pinaxproject.com/

Installation
=============

For development purposes. cd to cpc_project root::

    pip install --requirement requirements.txt
    python manage.py syncdb
    python manage.py reindex
    python manage.py runserver    
