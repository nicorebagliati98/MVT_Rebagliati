# Generated by Django 4.1 on 2022-10-21 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMVT', '0002_clientes_facturas_productos_delete_familiares'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturas',
            name='iva',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='monto_sin_iva',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='productos',
            name='iva',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='productos',
            name='precio_sin_iva',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]
