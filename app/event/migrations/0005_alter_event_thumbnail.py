# Generated by Django 3.2.17 on 2023-05-06 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_event_max_subscriber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='thumbnail',
            field=models.ImageField(default='default.png', upload_to='events/%Y/%M/', verbose_name='Feature image'),
        ),
    ]
