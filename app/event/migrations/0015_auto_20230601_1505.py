# Generated by Django 3.2.18 on 2023-06-01 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0006_alter_club_location'),
        ('shop', '0005_auto_20230505_0753'),
        ('event', '0014_auto_20230531_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='club.club'),
        ),
        migrations.AddField(
            model_name='event',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.shop'),
        ),
    ]
