import django_filters
from cards.models import Card


class CardFilter(django_filters.rest_framework.FilterSet):
    card_name = django_filters.CharFilter(lookup_expr='icontains')
    set_name = django_filters.CharFilter(lookup_expr='icontains')
    type = django_filters.CharFilter(lookup_expr='icontains')
    cost = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Card
        fields = '__all__'
