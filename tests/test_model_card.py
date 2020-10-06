import uuid
import pytest
from cards.models import Card

@pytest.mark.django_db
def test_card_create_and_str():
    test_card_data = { 'uuid': uuid.uuid4(), 'card_name': 'Test Card', 'set_name': 'Promo', 'type': 'Action', 'is_kingdom_card': 1, 'cost': '$3', 'card_text': 'Sample Card Text'}
    test_card = Card()
    for field in test_card_data:
        setattr(test_card, field, test_card_data[field])
    test_card.save()
    assert test_card_data['card_name'] == str(test_card)
