# Generated by Django 5.1 on 2024-08-29 19:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estampa', '0001_initial'),
        ('pedido', '0002_initial'),
        ('produto', '0007_rename_tipoproduto_categoriaproduto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='itempedido',
            name='estampa',
            field=models.ForeignKey(default=92, on_delete=django.db.models.deletion.CASCADE, to='estampa.estampa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itempedido',
            name='tamanho',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='produto.tamanho'),
            preserve_default=False,
        ),
    ]
