# Generated by Django 5.0.3 on 2024-04-05 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bibm", "0003_autor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="autor",
            name="comentario",
            field=models.TextField(blank=True, null=True),
        ),
    ]
