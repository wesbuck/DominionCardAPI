from cards.models import Card
from cards.serializers import CardSerializer
from cards.filters import CardFilter
from rest_framework import viewsets, mixins


# only extend the parts of ModelViewSet we want (omit Update & Destroy)
class CardList(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CardSerializer
    filter_class = CardFilter
    queryset = Card.objects.all()
