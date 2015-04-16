from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.utils.text import slugify
from django.utils.module_loading import import_string

from . import app_settings


@python_2_unicode_compatible
class AutomagicModel(models.Model):
    """
    Almost all code from: https://djangosnippets.org/snippets/2309/
    """

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse(self.get_absolute_url_alias(), kwargs={'pk': self.pk, 'slug': self.get_canonical_slug()})

    def get_create_url(self):
        return reverse(self.get_create_url_alias())

    def get_list_url(self):
        return reverse(self.get_list_url_alias())

    def get_delete_url(self):
        return reverse(self.get_delete_url_alias(), kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse(self.get_update_url_alias(), kwargs={'pk': self.pk})

    def get_url_regexp_prefix(self):
        return '%s/' % self._meta.model_name

    def get_absolute_url_regexp(self):
        return "^%s(?P<pk>\d+)-(?P<slug>[-\w\d]+)/$" % self.get_url_regexp_prefix()

    def get_create_url_regexp(self):
        return "^%screate/$" % self.get_url_regexp_prefix()

    def get_list_url_regexp(self):
        return "^%s$" % self.get_url_regexp_prefix()

    def get_delete_url_regexp(self):
        return "^%sdelete/(?P<pk>\d+)/$" % self.get_url_regexp_prefix()

    def get_update_url_regexp(self):
        return "^%supdate/(?P<pk>\d+)/$" % self.get_url_regexp_prefix()

    def get_absolute_url_alias(self):
        return "%s_%s_absolute" % (self._meta.app_label, self._meta.model_name)

    def get_create_url_alias(self):
        return '%s_%s_create' % (self._meta.app_label, self._meta.model_name)

    def get_list_url_alias(self):
        return "%s_%s_list" % (self._meta.app_label, self._meta.model_name)

    def get_delete_url_alias(self):
        return "%s_%s_delete" % (self._meta.app_label, self._meta.model_name)

    def get_update_url_alias(self):
        return "%s_%s_update" % (self._meta.app_label, self._meta.model_name)

    def get_urlpatterns(self, model_class, actions=[]):
        actions = actions if actions else app_settings.get('ACTIONS')
        urls = []
        for action in actions:
            url_param = 'absolute' if action == 'detail' else action  # detail is get_absolute_url
            urls.append(url(
                getattr(self, 'get_%s_url_regexp' % url_param)(),
                self.get_view('%sView' % action.capitalize(), model=model_class),
                name=getattr(self, 'get_%s_url_alias' % url_param)()
            ))
        return urls

    def get_view(self, name, **kwargs):
        """
        Makes the view overridable: app_label.views.ModelNameCreateView
        Fallback to default automagic class ex: automagic.views.AutomagicCreateView
        """
        try:
            class_path = '%s.views.%s%s' % (self._meta.app_label, self.__class__.__name__, name)
            view_class = import_string(class_path)
        except ImportError:
            class_path = 'automagic.views.Automagic%s' % name
            view_class = import_string(class_path)
        return view_class.as_view(**kwargs)

    def get_canonical_slug(self):
        """
        For braces.views.CanonicalSlugDetailMixin
        """
        if hasattr(self, 'slug'):
            return self.slug
        else:
            return slugify(self.__str__())

    def get_verbose_name(self):
        return self._meta.verbose_name

    def get_verbose_name_plural(self):
        return self._meta.verbose_name_plural

    def get_fields_and_values(self):
        return [(field, field.value_to_string(self)) for field in self._meta.fields]
