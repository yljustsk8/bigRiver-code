# Generated by Django 2.1 on 2018-09-07 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_info', '0015_remove_personal_info_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal_info',
            name='email',
            field=models.CharField(default='', max_length=50),
        ),
    ]
