# Generated by Django 3.1.7 on 2021-03-24 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210315_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='description',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='meal',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='meal',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='meal',
            name='portion',
            field=models.CharField(choices=[('0.7', '0.7'), ('1', '1')], max_length=50),
        ),
        migrations.AlterField(
            model_name='meal',
            name='price',
            field=models.PositiveIntegerField(max_length=50),
        ),
    ]
