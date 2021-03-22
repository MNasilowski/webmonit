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
    monit_content = models.BooleanField(default=False)
    monit_instance = models.BooleanField(default=False)
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
            description = f'HTTP error occurred: {http_err}'
            status = 999
            content = self.content
        except Exception as err:
            description = f'HTTP error occurred: {err}'
            status = 999
            content = self.content

        if self.monit_content:
            content_changes, message = self.is_content_changed(content)
        else:
            content_changes = False
            message = ""

        if self.status != status or content_changes:
            p = PageLog(
                page=self,
                status_change=False,
                status=status,
                content_changes=content_changes,
                description=description + message
            )

            p.save()

        self.content = content
        self.status = status
        self.save()
        return status

    def is_changed(self, name, url, frequency):
        """Check if name url frequency of the Page was changed"""
        message = ""
        if self.name != name:
            message += f"name was changed from {self.name} to {name} /n"
        if self.url != url:
            message += f"name was changed from {self.name} to {name} /n"
        if self.frequency != frequency:
            message += f"name was changed from {self.name} to {name} /n"
        return message != "", message

    def is_content_changed(self, content):
        """Check if page content was changed"""
        message = ""
        if self.content != content:
            message += "Page content was changed"
        return message != "", message

    def check_page(self):
        """Check availability,  """


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
