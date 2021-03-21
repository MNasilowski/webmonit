# Generated by Django 3.1.7 on 2021-03-21 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webmonit', '0002_page_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagelog',
            name='content_changes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pagelog',
            name='description',
            field=models.TextField(default='None'),
        ),
        migrations.AddField(
            model_name='pagelog',
            name='page_changes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pagelog',
            name='status_changes',
            field=models.BooleanField(default=False),
        ),
    ]
