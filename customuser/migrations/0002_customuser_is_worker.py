# Generated by Django 3.2.9 on 2021-11-15 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_worker',
            field=models.BooleanField(default=False),
        ),
    ]
