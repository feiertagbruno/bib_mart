# Generated by Django 5.0.3 on 2024-04-05 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bibm", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="endereco",
            name="comentario",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="genero",
            name="comentario",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="regiao",
            name="comentario",
            field=models.TextField(blank=True, null=True),
        ),
    ]