from cards.models import Card
from cards.serializers import CardSerializer
from cards.filters import CardFilter
from rest_framework import viewsets


class CardList(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    filter_class = CardFilter
    queryset = Card.objects.all()
