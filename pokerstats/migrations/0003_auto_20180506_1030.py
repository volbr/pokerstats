# Generated by Django 2.0.5 on 2018-05-06 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokerstats', '0002_player_current_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='teams',
            field=models.ManyToManyField(blank=True, null=True, to='pokerstats.Team'),
        ),
    ]