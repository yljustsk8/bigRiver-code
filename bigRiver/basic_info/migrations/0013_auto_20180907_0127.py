# Generated by Django 2.1 on 2018-09-07 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_info', '0012_auto_20180906_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal_info',
            name='email',
            field=models.CharField(default='1', max_length=50),
        ),
    ]
