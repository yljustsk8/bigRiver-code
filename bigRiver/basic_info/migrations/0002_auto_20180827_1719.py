# Generated by Django 2.0 on 2018-08-27 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_info', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personal_info',
            old_name='name2',
            new_name='name',
        ),
    ]
