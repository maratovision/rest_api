# Generated by Django 3.1.7 on 2021-03-16 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_employeeprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='date_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='date_start',
            field=models.DateTimeField(),
        ),
    ]