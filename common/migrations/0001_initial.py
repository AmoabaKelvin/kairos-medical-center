# Generated by Django 3.2.9 on 2021-11-30 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailDefaultValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=500)),
                ('message_body', models.TextField()),
            ],
            options={
                'verbose_name': 'EmailDefaultValue',
                'verbose_name_plural': 'EmailDefaultValues',
            },
        ),
    ]
