from django.db import models
import uuid

# Create your models here.
class Card(models.Model):
    uuid = models.CharField(max_length=64, null=True, default=uuid.uuid4, unique=True, error_messages={
        'unique': 'The uuid already exists'
    }, editable=False)
    card_name = models.CharField(max_length=64, null=False, unique=True, error_messages={
        'unique': 'The card name already exists'
    })
    set_name = models.CharField(max_length=32, null=False)
    type = models.CharField(max_length=64, null=False)
    is_kingdom_card = models.BooleanField(null=False)
    cost = models.CharField(max_length=4, null=False)
    card_text = models.TextField(max_length=1024, null=False)
    source = models.CharField(max_length=32, default='upload', editable=False)

    def __str__(self):
        return self.card_name
