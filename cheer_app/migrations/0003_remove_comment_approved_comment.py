# Generated by Django 2.2 on 2019-09-21 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cheer_app', '0002_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='approved_comment',
        ),
    ]