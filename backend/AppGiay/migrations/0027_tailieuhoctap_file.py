# Generated by Django 4.2.7 on 2024-12-15 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppGiay', '0026_tailieuhoctap'),
    ]

    operations = [
        migrations.AddField(
            model_name='tailieuhoctap',
            name='file',
            field=models.FileField(db_column='File', default='t', upload_to=''),
            preserve_default=False,
        ),
    ]
