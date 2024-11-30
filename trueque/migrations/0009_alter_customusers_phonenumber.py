# Generated by Django 5.1.3 on 2024-11-30 16:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trueque', '0008_alter_comic_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusers',
            name='phonenumber',
            field=models.CharField(blank=True, db_column='PhoneNumber', max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='El número de teléfono debe ser de exactamente 10 dígitos numéricos.', regex='^\\d{10}$')]),
        ),
    ]