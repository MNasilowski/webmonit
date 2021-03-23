from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_celery_beat.models import IntervalSchedule

from .models import Page, PageLog

@receiver(post_save, sender=Page)
def create_or_update_periodic_task(sender, instance, created, update_fields, **kwargs):
    if created:
        instance.setup_task()
    else:
        if instance.task is not None:
            pass

@receiver(pre_save, sender=Page)
def create_instance_change_log(sender, instance, **kwargs):
    if instance.id is None:
        pass
    else:
        previous = Page.objects.get(id=instance.id)
        inst_changed, message = previous.is_instance_changed(instance.name, instance.url, instance.frequency)
        t, _ = IntervalSchedule.objects.get_or_create(every=instance.frequency, period='minutes')
        if instance.monit_instance and inst_changed:
            p = PageLog(
                description=message,
                page=instance,
                status=instance.status,
                page_changes=inst_changed,
            )
            p.save()
        if instance.frequency != previous.frequency:
            t, _ = IntervalSchedule.objects.get_or_create(every=instance.frequency, period='minutes')
            instance.task.enabled = True
            instance.task.interval = t
            instance.task.save()
