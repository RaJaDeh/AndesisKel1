# Generated by Django 4.2.1 on 2023-05-29 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0016_alter_book_isbn'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentextra',
            old_name='branch',
            new_name='Asal_Daerah',
        ),
        migrations.RenameField(
            model_name='studentextra',
            old_name='enrollment',
            new_name='Asal_Universitas',
        ),
    ]
