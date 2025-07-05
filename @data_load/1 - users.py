from django.contrib.auth.models import Group
sco_staff=Group.objects.create(name="SCO STAFF")

from django.contrib.auth.models import User
scouser = User.objects.create_user(username="sco", password="scobernai", is_staff=True)
scouser.groups.add(sco_staff)
arnaud = User.objects.create_user("arnaud.brand@gmail.com", "arnaud.brand@gmail.com", "scobernai", is_staff=True)
arnaud.groups.add(sco_staff)
anne = User.objects.create_user("anne.schreck@free.fr", "anne.schreck@free.fr", "scobernai", is_staff=True)
anne.groups.add(sco_staff)
claudine = User.objects.create_user("claudine.sco@orange.fr", "claudine.sco@orange.fr", "scobernai", is_staff=True)
claudine.groups.add(sco_staff)
olivier = User.objects.create_user("olivier.pflieger@free.fr", "olivier.pflieger@free.fr", "scobernai", is_staff=True)
olivier.groups.add(sco_staff)
michel = User.objects.create_user("michel.dufoir@gmail.com", "michel.dufoir@gmail.com", "scobernai", is_staff=True)
michel.groups.add(sco_staff)
cyril = User.objects.create_user("lagneaux.cyril@yahoo.fr", "lagneaux.cyril@yahoo.fr", "scobernai", is_staff=True)
cyril.groups.add(sco_staff)
philippe = User.objects.create_user("ph.aptel@gmail.com", "ph.aptel@gmail.com", "scobernai", is_staff=True)
philippe.groups.add(sco_staff)
sbastien = User.objects.create_user("metz.seb@gmail.com", "metz.seb@gmail.com", "scobernai", is_staff=True)
sbastien.groups.add(sco_staff)

