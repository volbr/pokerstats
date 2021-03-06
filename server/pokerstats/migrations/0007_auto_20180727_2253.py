# Generated by Django 2.0.5 on 2018-07-27 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokerstats', '0006_auto_20180727_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameresult',
            name='best_combination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='combination_results', to='pokerstats.Round'),
        ),
        migrations.AlterField(
            model_name='gameresult',
            name='best_winning',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winning_results', to='pokerstats.Round'),
        ),
    ]
