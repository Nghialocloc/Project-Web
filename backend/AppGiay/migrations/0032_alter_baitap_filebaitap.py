# Generated by Django 4.2.7 on 2024-12-19 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppGiay', '0031_alter_baitap_filebaitap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baitap',
            name='filebaitap',
            field=models.FileField(db_column='FileBaiTap', upload_to='baitap_files/<django.db.models.fields.related.ForeignKey>'),
        ),
    ]
