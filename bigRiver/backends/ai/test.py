import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

from basic_info.models import personal_info
