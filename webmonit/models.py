import json
import requests
from django.db import models
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from requests.exceptions import HTTPError

from django.utils import timezone
import datetime

class Page(models.Model):
    name = models.TextField(max_length=50)
    url = models.TextField()
    status = models.IntegerField(default=0)
    frequency = models.IntegerField(default=60)
    content = models.JSONField
    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def setup_task(self):
        t, _ = IntervalSchedule.objects.get_or_create(every=self.frequency, period='minutes')
        self.task = PeriodicTask.objects.create(
            name=self.name,
            task='check_page',
            interval=t,
            args=json.dumps([self.id]),
            start_time=timezone.now()
        )
        self.save()

    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def __str__(self):
        return self.url

    def is_available(self):
        """Check status of the webpage"""
        try:
            response = requests.get(self.url)
            status = response.status_code
            content = response.text
            description = response.reason
        except HTTPError as http_err:
            description = (f'HTTP error occurred: {http_err}')
            status = 999
            content = self.content
        except Exception as err:
            description = (f'HTTP error occurred: {err}')
            status = 999
            content = self.content

        if self.status != status:
            p = PageLog(
                page=self,
                status=status,
                status_changes=True,
                description=description
            )
            p.save()

        self.content = content
        self.status = status
        self.save()

        return status


class PageLog(models.Model):
    def __STR__(self):
        return f'{self.page} status: {self.status}'

    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    check_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    status = models.IntegerField(default=200)
    content_changes = models.BooleanField(default=False)
    page_changes = models.BooleanField(default=False)
    status_changes = models.BooleanField(default=False)
    description = models.TextField(default='None')