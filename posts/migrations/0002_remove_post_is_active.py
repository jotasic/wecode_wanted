# Generated by Django 3.2.8 on 2021-10-21 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_active',
        ),
    ]
