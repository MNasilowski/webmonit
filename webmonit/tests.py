from django.test import TestCase
from .models import Page
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class PageModelTests(TestCase):

    def test_page_is_available_working_url(self):
        """Check if the is_available method return 200 for available url"""
        new_page = Page(name="test", url = "https://www.onet.pl")
        new_page.save()
        self.assertEqual(new_page.is_available(), 200)

    def test_page_is_available_not_working_url(self):
        """Check if the is_available method return 200 for unexisting url"""
        new_page = Page(name="test", url="https://abc.abc.abc")
        new_page.save()
        self.assertNotEqual(new_page.is_available(), 200)

    def test_change_frequency_change_task(self):
        """Created page create new task"""
        new_page = Page(name="test", url="https://www.onet.pl")
        new_page.frequency = 500
        new_page.save()
        new_task = PeriodicTask.objects.get(name='test')
        self.assertEqual(new_task.interval.every, IntervalSchedule(every=new_page.frequency, period='minutes').every)

    def test_new_page_new_task(self):
        """Created page create new task"""
        new_page = Page(name="test", url="https://www.onet.pl")
        new_page.save()
        new_task = PeriodicTask.objects.filter(name='test')
        self.assertIsNotNone(new_task)

    def test_page_deleted_task_deleted(self):
        self.assertEqual(1, 1)

# TO DO correct test and add some more