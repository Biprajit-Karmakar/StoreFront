# Generated by Django 4.1.3 on 2022-12-04 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_product_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
