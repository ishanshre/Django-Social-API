# Generated by Django 4.1.7 on 2023-03-22 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_post', '0003_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='user',
            new_name='created_by',
        ),
    ]
