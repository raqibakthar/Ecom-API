# Generated by Django 5.0.2 on 2024-02-13 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
    ]