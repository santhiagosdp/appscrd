# Generated by Django 3.2.11 on 2023-03-18 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startgame', '0003_auto_20230317_2106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='time',
            old_name='Jogador',
            new_name='jogador',
        ),
        migrations.AlterField(
            model_name='time',
            name='cor_time',
            field=models.CharField(choices=[('gree', 'Verde'), ('yellow', 'Amarelo'), ('blue', 'Azul'), ('red', 'Vermelho')], max_length=6),
        ),
    ]
