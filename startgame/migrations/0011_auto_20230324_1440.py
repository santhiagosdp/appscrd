# Generated by Django 3.2.18 on 2023-03-24 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startgame', '0010_alter_jogador_posicao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pelada',
            name='local',
        ),
        migrations.RemoveField(
            model_name='pelada',
            name='valor_jogador',
        ),
    ]
