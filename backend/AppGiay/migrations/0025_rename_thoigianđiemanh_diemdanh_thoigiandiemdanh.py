# Generated by Django 4.2.7 on 2024-12-14 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppGiay', '0024_buoihoc_diemdanh'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diemdanh',
            old_name='thoigianđiemanh',
            new_name='thoigiandiemdanh',
        ),
    ]
