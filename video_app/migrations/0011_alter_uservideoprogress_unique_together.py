# Generated by Django 5.1.7 on 2025-03-31 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0010_alter_uservideoprogress_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='uservideoprogress',
            unique_together=set(),
        ),
    ]
