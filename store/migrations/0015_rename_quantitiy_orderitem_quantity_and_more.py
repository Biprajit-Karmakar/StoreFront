# Generated by Django 4.1.3 on 2023-01-16 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_customer_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='quantitiy',
            new_name='quantity',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='store.order'),
        ),
    ]