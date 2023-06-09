# Generated by Django 3.2.18 on 2023-04-28 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('notaseasy', '0002_auto_20230428_1326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notafiscal',
            name='arquivo',
        ),
        migrations.AddField(
            model_name='notafiscal',
            name='content_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notafiscal',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('arquivo', models.FileField(upload_to='arquivos/')),
                ('habilitado', models.BooleanField(default=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
