# Generated by Django 4.2.7 on 2023-11-14 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gardenplaner', '0003_alter_color_description_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='name_en',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='plant',
            name='name_lt',
            field=models.CharField(max_length=100),
        ),
    ]
