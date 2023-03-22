# Generated by Django 3.2.18 on 2023-03-22 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startgame', '0006_alter_time_cor_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pelada',
            name='tempo_pelada',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='time',
            name='cor_time',
            field=models.CharField(choices=[('green', 'Verde'), ('yellow', 'Amarelo'), ('blue', 'Azul'), ('black', 'Preto'), ('orange', 'Laranja'), ('red', 'Vermelho')], max_length=6),
        ),
    ]
