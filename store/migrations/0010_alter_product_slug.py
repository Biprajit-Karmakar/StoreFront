# Generated by Django 4.1.3 on 2022-11-27 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(),
        ),
    ]