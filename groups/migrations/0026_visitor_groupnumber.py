# Generated by Django 3.1.2 on 2020-12-07 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0025_auto_20201204_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='Groupnumber',
            field=models.CharField(max_length=300, null=True),
        ),
    ]