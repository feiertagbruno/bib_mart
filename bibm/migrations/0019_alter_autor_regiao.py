# Generated by Django 5.0.3 on 2024-07-13 01:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibm', '0018_rename_invisivel_livro_deletado_anotacao_deletado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autor',
            name='regiao',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='bibm.regiao'),
        ),
    ]
