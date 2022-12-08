# Generated by Django 4.1.3 on 2022-12-04 14:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_collection_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
