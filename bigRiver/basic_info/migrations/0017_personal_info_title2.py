# Generated by Django 2.1 on 2018-09-10 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_info', '0016_personal_info_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal_info',
            name='title2',
            field=models.IntegerField(default=0),
        ),
    ]
