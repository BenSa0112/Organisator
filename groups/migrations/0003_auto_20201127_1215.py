# Generated by Django 3.1.2 on 2020-11-27 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_grouplist_group_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouplist',
            name='group_size',
            field=models.IntegerField(null=True),
        ),
    ]
