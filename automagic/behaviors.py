"""
http://blog.kevinastone.com/django-model-behaviors.html
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class Ownerable(models.Model):
    user = models.ForeignKey(get_user_model())

    class Meta:
        abstract = True


class Sluggable(models.Model):
    slug = models.SlugField(_('slug'))

    class Meta:
        abstract = True


class Publishable(models.Model):
    published = models.DateTimeField(_('published date'), null=True)

    class Meta:
        abstract = True


class Timestampable(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True