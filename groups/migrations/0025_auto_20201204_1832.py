# Generated by Django 3.1.2 on 2020-12-04 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0024_auto_20201204_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intervalldate',
            name='end_date',
            field=models.DateField(blank=True),
        ),
    ]
