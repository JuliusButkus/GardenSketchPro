# Generated by Django 4.2.7 on 2023-11-14 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gardenplaner', '0008_alter_photo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/', verbose_name='add image'),
        ),
    ]
