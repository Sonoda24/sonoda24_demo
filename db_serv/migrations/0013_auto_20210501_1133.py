# Generated by Django 3.0.8 on 2021-05-01 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_serv', '0012_auto_20210430_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='my_svg',
            name='cnsvg_nk',
            field=models.IntegerField(blank=True, null=True, verbose_name='csvg_nk'),
        ),
        migrations.AddField(
            model_name='my_svg',
            name='name',
            field=models.CharField(blank=True, max_length=10, verbose_name='著者'),
        ),
    ]
