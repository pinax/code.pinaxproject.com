#!/bin/bash

source /home/pinax/virtualenvs/cpc/bin/activate
cd /home/pinax/webapps/code.pinaxproject.com/cpc_project
./manage.py emit_notices >> /home/pinax/webapps/code.pinaxproject.com/logs/cron_notices.log 2>&1
./manage.py send_mail >> /home/pinax/webapps/code.pinaxproject.com/logs/cron_mail.log 2>&1