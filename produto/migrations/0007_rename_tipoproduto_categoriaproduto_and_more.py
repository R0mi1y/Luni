# Generated by Django 5.1 on 2024-08-29 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0006_add_default_sizes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TipoProduto',
            new_name='CategoriaProduto',
        ),
        migrations.RenameField(
            model_name='produto',
            old_name='tipos',
            new_name='categorias',
        ),
    ]
