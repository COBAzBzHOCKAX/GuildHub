# Generated by Django 5.0.6 on 2024-06-17 00:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('response_board', '0003_alter_response_date_status_change'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='text',
            field=models.TextField(help_text='Enter your text here (1000 characters max)', validators=[django.core.validators.MaxLengthValidator(1000)], verbose_name='Text'),
        ),
    ]
