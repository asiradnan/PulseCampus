# Generated by Django 5.2 on 2025-05-14 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='vote',
            field=models.IntegerField(default=0),
        ),
    ]
