from django.db import models
from django.test import TestCase
from .models import AutomagicModel


class MyFooModel(AutomagicModel):
    title = models.CharField(max_length=20)

    def __unicode__(self):
        return self.title

class AutomagicModelTest(TestCase):

    def test_automagic_model(self):
        self.assertTrue(MyFooModel.objects.create(title='Foobar'))

    def test_get_canonical_slug(self):
        foo_url = MyFooModel.objects.create(title='Foobar')
        self.assertEquals(foo_url.get_canonical_slug(), 'foobar')
        self.assertTrue(isinstance(foo_url.get_canonical_slug(), str), True)
        self.assertTrue(isinstance(foo_url.get_fields_and_values(), list))
