# Generated by Django 3.2.4 on 2021-11-02 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_rename_enable_protection_authtoggle_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authtoggle',
            old_name='On',
            new_name='protected',
        ),
    ]
