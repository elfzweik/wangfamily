# Generated by Django 3.2.12 on 2022-05-04 04:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0016_alter_blogdetailpage_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogdetailpage',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
