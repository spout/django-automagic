"""
https://nicolas.perriault.net/code/2011/clever-settings/
"""
from django.conf import settings

app_settings = dict({
    'ACTIONS': ['create', 'detail', 'update', 'delete', 'list'],
    'STR_ATTRS': ['title', 'name'],
    'SLUG_ATTR': 'slug',
}, **getattr(settings, 'AUTOMAGIC_CONFIG', {}))