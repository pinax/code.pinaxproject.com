from django.core.management.base import BaseCommand
from django.db import connections

from django.contrib.auth.models import User

from emailconfirmation.models import EmailAddress


class Command(BaseCommand):
    help = "Migrates the old CPC database"
    
    def handle(self, *args, **options):
        cursors = {
            "default": connections["default"].cursor(),
            "old": connections["old"].cursor(),
        }
        
        # User model
        
        cursors["old"].execute("SELECT * FROM auth_user ORDER BY id")
        for row in cursors["old"].fetchall():
            if User.objects.filter(username=row[1]).exists():
                continue
            u = User()
            u.id = row[0]
            u.username = row[1]
            u.first_name = row[2]
            u.last_name = row[3]
            u.email = row[4]
            u.password = row[5]
            u.is_staff = row[6]
            u.is_active = row[7]
            u.is_superuser = row[8]
            u.last_login = row[9]
            u.date_joined = row[10]
            u.save()
            EmailAddress(user=u, email=u.email, verified=True, primary=True).save()
            print "[User] migrated %s" % u.username
        cursors["default"].execute("SELECT setval('auth_user_id_seq', (SELECT max(id) FROM auth_user))")
