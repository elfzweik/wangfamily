# Generated by Django 4.0.7 on 2022-09-23 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0006_mycomment_save_casued_by_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mycomment',
            old_name='save_casued_by_comment',
            new_name='save_caused_by_comment',
        ),
    ]
