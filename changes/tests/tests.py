__all__ = [
    'ChangesTestCase',
    'ChangesUserTestCase',
    'ChangesMixinTestCase'
]


import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.tests.utils import skipIfCustomUser
from django.utils.timezone import utc

from ..models import Change

from models import ChangesTestModel


User = get_user_model()


class ChangesTestCase(TestCase):
    def setUp(self):
        self.subject = ChangesTestModel.objects.create(name='TestModel')

    def test_add_get_change_for_object(self):
        when = datetime.datetime(1984, 11, 15, 10).replace(tzinfo=utc)
        c1 = Change.objects.add_change_for_object(self.subject, why='Test',
                                                  when=when)
        c2 = Change.objects.add_change_for_object(self.subject)
        self.assertEqual(c1.c_obj, self.subject)
        self.assertEqual(c1.when, when)

        self.assertEqual(
            [c2, c1],
            list(Change.objects.get_changes_for_object(self.subject))
        )
        self.assertEqual(
            [c2, c1],
            list(Change.objects.get_anonymous_changes())
        )


@skipIfCustomUser
class ChangesUserTestCase(TestCase):
    def setUp(self):
        self.actor = User.objects.create(username='actor')
        self.subject = ChangesTestModel.objects.create(name='TestModel')

    def test_add_get_change_for_object(self):
        when = datetime.datetime(1984, 11, 15, 10).replace(tzinfo=utc)
        c1 = Change.objects.add_change_for_object(self.subject, who=self.actor,
                                                  why='Test', when=when)
        c2 = Change.objects.add_change_for_object(self.subject)
        self.assertEqual(c1.who, self.actor)
        self.assertEqual(c1.c_obj, self.subject)
        self.assertEqual(c1.when, when)

        self.assertEqual(
            [],
            list(Change.objects.get_changes_for_object(self.actor))
        )
        self.assertEqual(
            [c2, c1],
            list(Change.objects.get_changes_for_object(self.subject))
        )
        self.assertEqual(
            [c1],
            list(Change.objects.get_changes_by_user(self.actor))
        )
        self.assertEqual(
            [c2],
            list(Change.objects.get_anonymous_changes())
        )


class ChangesMixinTestCase(TestCase):
    def setUp(self):
        self.subject = ChangesTestModel.objects.create(name='TestModel')

    def test_reverse_relation(self):
        self.subject.add_change(why='Time for a change')
        self.assertEqual(
            list(self.subject.changes.all()),
            list(Change.objects.all())
        )

    def test_save(self):
        self.subject.name = 'New Name'
        self.subject.save(changed=True, why='For a change')
        all_changes = list(Change.objects.all())
        self.assertEqual(
            list(Change.objects.get_changes_for_object(self.subject)),
            list(all_changes)
        )
        self.subject.save()
        self.assertEqual(
            list(Change.objects.get_changes_for_object(self.subject)),
            list(all_changes)
        )

    def test_add_get_changes(self):
        self.subject.add_change(why='Because')
        self.assertEqual(
            list(self.subject.get_changes()),
            list(Change.objects.get_changes_for_object(self.subject)),
            list(Change.objects.filter(why='For a change'))
        )
