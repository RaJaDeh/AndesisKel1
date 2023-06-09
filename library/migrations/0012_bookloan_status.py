# Generated by Django 4.2 on 2023-05-24 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_bookloan'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookloan',
            name='status',
            field=models.CharField(choices=[('waiting_approval', 'Menunggu Konfirmasi Peminjaman'), ('borrowed', 'Dipinjam'), ('waiting_return_confirmation', 'Menunggu Konfirmasi Pengembalian'), ('returned', 'Dikembalikan')], default='waiting_approval', max_length=30),
        ),
    ]
