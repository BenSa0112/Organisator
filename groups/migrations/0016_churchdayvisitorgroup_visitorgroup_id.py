# Generated by Django 3.1.2 on 2020-12-01 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0015_auto_20201201_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='churchdayvisitorgroup',
            name='visitorgroup_id',
            field=models.IntegerField(null=True),
        ),
    ]