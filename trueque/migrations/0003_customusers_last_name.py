# Generated by Django 5.1.3 on 2024-11-25 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trueque', '0002_customusers_is_active_customusers_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusers',
            name='last_name',
            field=models.TextField(blank=True, db_column='LastName', null=True),
        ),
    ]
