# Generated by Django 2.0.2 on 2018-02-25 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmify', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='last_synced',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
