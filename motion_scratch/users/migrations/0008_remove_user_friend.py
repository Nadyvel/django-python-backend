# Generated by Django 3.0 on 2019-12-20 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20191219_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='friend',
        ),
    ]
