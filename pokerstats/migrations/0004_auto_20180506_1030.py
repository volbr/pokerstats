# Generated by Django 2.0.5 on 2018-05-06 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokerstats', '0003_auto_20180506_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='teams',
            field=models.ManyToManyField(blank=True, to='pokerstats.Team'),
        ),
    ]