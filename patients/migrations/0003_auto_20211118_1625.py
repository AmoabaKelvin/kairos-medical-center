# Generated by Django 3.2.9 on 2021-11-18 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_auto_20211118_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='tests_to_carry',
        ),
        migrations.AddField(
            model_name='patient',
            name='tests_to_carry',
            field=models.TextField(default='Malaria', max_length=500),
            preserve_default=False,
        ),
    ]
