# Generated by Django 5.2 on 2025-05-04 08:23

import PulseCampus.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(max_length=10, unique=True, validators=[PulseCampus.validators.id_validate]),
        ),
    ]
