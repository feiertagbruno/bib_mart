# Generated by Django 5.0.3 on 2024-04-07 19:36

import bibm.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bibm", "0005_livro"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="autor",
            options={"verbose_name_plural": "autores"},
        ),
        migrations.AlterModelOptions(
            name="endereco",
            options={"verbose_name": "Endereço"},
        ),
        migrations.AlterModelOptions(
            name="genero",
            options={"verbose_name": "gênero"},
        ),
        migrations.AlterModelOptions(
            name="regiao",
            options={"verbose_name_plural": "regiões"},
        ),
        migrations.RemoveField(
            model_name="autor",
            name="nome",
        ),
        migrations.AddField(
            model_name="autor",
            name="prim_nome",
            field=models.CharField(default="Novo", max_length=65),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="autor",
            name="ult_nome",
            field=models.CharField(default="Autor", max_length=65),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="livro",
            name="lendo",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="livro",
            name="planejamento",
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="endereco",
            name="codigo",
            field=models.CharField(
                max_length=5, validators=[bibm.models.validacao_endereco]
            ),
        ),
        migrations.AlterField(
            model_name="livro",
            name="classificacao",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (1, "1"),
                    (2, "2"),
                    (3, "3"),
                    (4, "4"),
                    (5, "5"),
                    (6, "6"),
                    (7, "7"),
                    (8, "8"),
                    (9, "9"),
                    (10, "10"),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="livro",
            name="comentario",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="livro",
            name="data_leitura",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="livro",
            name="editora",
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.CreateModel(
            name="Historico",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data_ini", models.DateTimeField(auto_now_add=True)),
                ("data_fim", models.DateTimeField(auto_now=True)),
                ("terminou", models.BooleanField(default=True)),
                (
                    "livro",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="bibm.livro"
                    ),
                ),
            ],
        ),
    ]