# Generated by Django 3.1.7 on 2021-03-16 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20210317_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='date_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='date_start',
            field=models.DateField(blank=True, null=True),
        ),
    ]
