# Generated by Django 5.1.7 on 2025-03-28 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.CharField(choices=[('romatic', 'romatic'), ('fanatsy', 'fanatsy'), ('action', 'action'), ('romantic', 'romantic'), ('documentary', 'documentary'), ('comedy', 'comedy')], max_length=255),
        ),
    ]
