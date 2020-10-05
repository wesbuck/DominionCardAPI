from cards.models import Card
from cards.serializers import CardSerializer
from cards.filters import CardFilter
from rest_framework import viewsets, mixins, status

from rest_framework.decorators import api_view # for api_view
from rest_framework.response import Response # for api_view
from rest_framework.reverse import reverse # for api_view

from rest_framework.views import APIView
from rest_framework.response import Response
from random import randint
from django.core import serializers
from django.forms.models import model_to_dict
import json


# show API entry points
@api_view(['GET']) # new
def api_root(request, format=None):
    return Response({
        'Documentation': 'https://documenter.getpostman.com/view/5603098/RWguxcDR',
        'Get a Random Card': reverse('Random', request=request, format=format),
        'Get a Kingdom Card': reverse('Kingdom', request=request, format=format),
        'Get a Set of 10 Cards': reverse('CardSet', request=request, format=format),
        'Get All Cards': reverse('All', request=request, format=format),
    })

def get_random_card_pk():
    return Card.objects.order_by("?").first().pk
    
def get_random_kingdom_card_pk():
    return Card.objects.filter(is_kingdom_card=1).order_by("?").first().pk

# only extend the parts of ModelViewSet we want
class CardList(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    serializer_class = CardSerializer
    filterset_class = CardFilter
    queryset = Card.objects.all()

    def destroy(self, request, pk):
        card = Card.objects.get(id=pk)
        if card.source != 'upload':
            return Response('Only manually created cards can be deleted.', status=status.HTTP_400_BAD_REQUEST)
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk, *args, **kwargs):
        card = Card.objects.get(id=pk)
        if card.source != 'upload':
            return Response('Only manually created cards can be updated.', status=status.HTTP_400_BAD_REQUEST)
        return super(CardList, self).update(request, *args, **kwargs)

    def partial_update(self, request, pk, *args, **kwargs):
        card = Card.objects.get(id=pk)
        if card.source != 'upload':
            return Response('Only manually created cards can be updated.', status=status.HTTP_400_BAD_REQUEST)
        return super(CardList, self).partial_update(request, pk, *args, **kwargs)


# get a single random card
class Random(APIView):

    def get(self, request):
        rand = get_random_card_pk()
        card = Card.objects.get(pk=rand)
        return Response(json.loads(json.dumps(model_to_dict(card))))


# get a single random kingdom card
class Kingdom(APIView):

    def get(self, request):
        rand = get_random_kingdom_card_pk()
        card = Card.objects.get(pk=rand)
        return Response(json.loads(json.dumps(model_to_dict(card))))


# get 10 unique random kingdom cards
class CardSet(APIView):

    def get(self, request):
        arr = []  # list of cards
        while len(arr) < 10:
            rand = get_random_kingdom_card_pk()
            if rand not in arr:  # ensure no duplicates
                arr.append(rand)
        cards = Card.objects.filter(pk__in=arr)
        raw_data = json.loads(serializers.serialize('json', cards))
        output = [d['fields'] for d in raw_data]  # extract inner 'fields' dicts
        return Response(json.loads(json.dumps(output)))

# get all kingdom cards
class All(APIView):

    def get(self, request):
        cards = Card.objects.all().filter(is_kingdom_card=1)
        raw_data = json.loads(serializers.serialize('json', cards))
        output = [d['fields'] for d in raw_data]  # extract inner 'fields' dicts
        return Response(json.loads(json.dumps(output)))
