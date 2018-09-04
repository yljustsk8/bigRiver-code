# Generated by Django 2.0 on 2018-09-04 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestID', models.CharField(default='', max_length=10)),
                ('senderID', models.CharField(default='', max_length=10)),
                ('receiverID', models.CharField(default='', max_length=10)),
                ('date', models.CharField(default='', max_length=10)),
                ('type', models.IntegerField(default=-1)),
                ('content', models.CharField(default='', max_length=100)),
                ('dealed', models.BooleanField(default=False)),
                ('result', models.IntegerField(default=-1)),
            ],
        ),
    ]
