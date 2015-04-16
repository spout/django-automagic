from django.contrib import admin

from .utils import get_app_models


def register_app_models(app_label, models_list=[]):
    admin.site.register(get_app_models(app_label, models_list))
