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
            if instance.frequency != instance.task.interval.every:
                t, _ = IntervalSchedule.objects.get_or_create(every=instance.frequency, period='minutes')
                if instance.monit_instance:
                    p = PageLog(
                        description=f"Post save Monit frequency was changed from {instance.task.interval.every} to {instance.frequency}",
                        page=instance,
                        status=instance.status,
                        page_changes = True,
                    )
                    p.save()
                instance.task.enabled = True
                instance.task.interval = t
                instance.task.save()

#@receiver(pre_save, sender=Page)
#def create_instance_change_log(sender, instance, create, **kwargs):
#    pass
