# Generated by Django 3.1.2 on 2020-12-01 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0011_visitorgroup_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorgroup',
            name='data',
            field=models.JSONField(null=True),
        ),
    ]
