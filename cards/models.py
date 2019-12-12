from django.db import models


# Create your models here.
class Card(models.Model):
    uuid = models.CharField(max_length=128, null=True)
    card_name = models.CharField(max_length=64, null=True)
    set_num = models.IntegerField(null=True)
    set_name = models.CharField(max_length=32, null=True)
    type = models.CharField(max_length=64, null=True)
    cost = models.CharField(max_length=4, null=True)
    card_text = models.TextField(max_length=1024, null=True)

    def __str__(self):
        return self.card_name
