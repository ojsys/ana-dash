# Generated by Django 5.1.1 on 2024-09-21 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_customuser_country'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='location',
            new_name='state',
        ),
    ]
