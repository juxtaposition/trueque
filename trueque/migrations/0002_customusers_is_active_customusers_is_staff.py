# Generated by Django 5.1.3 on 2024-11-25 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trueque', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusers',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customusers',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]