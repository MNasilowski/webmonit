from celery import shared_task
from .models import Page


@shared_task(name='check_page')
def check_page(page_id):
    p = Page.objects.get(id=page_id)
    p.check_page()