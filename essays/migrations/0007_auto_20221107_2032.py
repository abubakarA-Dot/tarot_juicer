# Generated by Django 3.2.12 on 2022-11-07 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essays', '0006_auto_20220119_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='bibliographyarticle',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contentchanges',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
