# Generated by Django 2.0.5 on 2018-05-13 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokerstats', '0014_remove_rebuy_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rebuy',
            name='player',
        ),
        migrations.AlterField(
            model_name='rebuy',
            name='round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokerstats.RoundResult'),
        ),
    ]
