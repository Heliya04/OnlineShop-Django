# Generated by Django 5.1.2 on 2024-12-04 18:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_amount',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='price',
            new_name='total_amount',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Shop.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]