# Generated by Django 4.1.3 on 2022-11-28 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taggeditem',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
