# Generated by Django 3.2.18 on 2023-03-22 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startgame', '0005_auto_20230317_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time',
            name='cor_time',
            field=models.CharField(choices=[('green', 'Verde'), ('yellow', 'Amarelo'), ('blue', 'Azul'), ('red', 'Vermelho')], max_length=6),
        ),
    ]
