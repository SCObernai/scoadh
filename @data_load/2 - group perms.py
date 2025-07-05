

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
sco_staff=Group.objects.get(name="SCO STAFF")
rights=('view', 'change', 'delete', 'add')
for app in ('adh', 'hab', 'glo', 'lic', 'act', 'pan'):
    for m in list(dict(apps.all_models[app]).keys()):
        if '_' in m:
            continue
        for r in rights:
            p=Permission.objects.get_by_natural_key(f"{r}_{m}", app, m)
            sco_staff.permissions.add(p)
