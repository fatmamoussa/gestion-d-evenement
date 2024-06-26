# Generated by Django 3.2.17 on 2023-05-05 07:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('club', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='club',
            name='description',
            field=tinymce.models.HTMLField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='club',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name of the store'),
        ),
        migrations.AlterField(
            model_name='club',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='club',
            name='thumbnail',
            field=models.ImageField(default='default.png', upload_to='shops/%Y/%M/', verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='club',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
