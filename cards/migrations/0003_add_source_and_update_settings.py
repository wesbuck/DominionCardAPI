# Generated by Django 3.1.2 on 2020-10-05 03:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_card_is_kingdom_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='source',
            field=models.CharField(default='upload', editable=False, max_length=32),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_name',
            field=models.CharField(error_messages={'unique': 'The card name already exists'}, max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_text',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='card',
            name='cost',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='card',
            name='set_name',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='card',
            name='set_num',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='card',
            name='type',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='card',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, error_messages={'unique': 'The uuid already exists'}, max_length=64, null=True, unique=True),
        ),
    ]