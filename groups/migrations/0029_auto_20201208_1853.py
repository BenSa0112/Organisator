# Generated by Django 3.1.2 on 2020-12-08 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0028_auto_20201208_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='address',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='visitor',
            name='number',
            field=models.CharField(default='', max_length=100),
        ),
    ]