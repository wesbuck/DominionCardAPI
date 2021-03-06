# Generated by Django 3.1.2 on 2020-10-06 01:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_add_source_and_update_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='is_kingdom_card',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='card',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, error_messages={'unique': 'The uuid already exists'}, max_length=64, null=True, unique=True),
        ),
    ]
