# Generated by Django 2.0 on 2018-09-06 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_info', '0011_auto_20180906_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company_info',
            name='adminID',
            field=models.CharField(default='', max_length=100),
        ),
    ]
