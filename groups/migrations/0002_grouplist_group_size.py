# Generated by Django 3.1.2 on 2020-11-27 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouplist',
            name='group_size',
            field=models.IntegerField(max_length=200, null=True),
        ),
    ]
