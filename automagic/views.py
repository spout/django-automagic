from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelform_factory
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.module_loading import import_string

from braces.views import CanonicalSlugDetailMixin, FormMessagesMixin, JSONResponseMixin, AjaxResponseMixin


class AutomagicViewMixin(JSONResponseMixin, AjaxResponseMixin):
    form_invalid_message = _("Please correct the errors below.")

    def get_template_names(self):
        template_names = super(AutomagicViewMixin, self).get_template_names()
        template_names += ['automagic/%s.html' % self.template_name_suffix[1:]]

        return template_names

    def get_form_class(self):
        """
        Makes forms overridables: app_label.forms.ModelNameForm
        Fallback to AutomagicForm
        """
        if self.form_class:
            return self.form_class

        try:
            class_path = '%s.forms.%sForm' % (self.model._meta.app_label, self.model.__name__)
            form = import_string(class_path)
        except ImportError:
            class_path = 'automagic.forms.AutomagicForm'
            form = import_string(class_path)

        return modelform_factory(self.model, form=form)


class AutomagicListView(AutomagicViewMixin, ListView):
    pass


class AutomagicDetailView(AutomagicViewMixin, CanonicalSlugDetailMixin, DetailView):
    pass


class AutomagicCreateView(AutomagicViewMixin, FormMessagesMixin, CreateView):
    template_name_suffix = '_form_create'
    form_valid_message = _("Record was created successfully.")


class AutomagicUpdateView(AutomagicViewMixin, FormMessagesMixin, UpdateView):
    template_name_suffix = '_form_update'
    form_valid_message = _("Record was updated successfully.")


class AutomagicDeleteView(AutomagicViewMixin, DeleteView):

    def delete(self, request, *args, **kwargs):
        messages.success(request, _("Record was deleted successfully."))
        return super(AutomagicDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("%s_%s_list" % (self.object._meta.app_label, self.object._meta.model_name))
