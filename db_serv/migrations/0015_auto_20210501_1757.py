# Generated by Django 3.0.8 on 2021-05-01 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_serv', '0014_auto_20210501_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='my_data',
            name='cnsvg_tags',
            field=models.CharField(blank=True, max_length=200, verbose_name='cnsvg_tags'),
        ),
    ]
