# Generated by Django 3.1.4 on 2020-12-18 16:01

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20201126_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='myfield',
            field=markdownx.models.MarkdownxField(null=True),
        ),
    ]
