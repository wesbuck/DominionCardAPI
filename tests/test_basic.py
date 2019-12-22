import uuid
import pytest

@pytest.fixture
def test_password():
   return 'strong-test-pass'

@pytest.fixture
def create_user(db, django_user_model, test_password):
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return django_user_model.objects.create_user(**kwargs)
   return make_user

@pytest.fixture
def api_client():
   from rest_framework.test import APIClient
   return APIClient()

from django.core.management import call_command
@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'tests/testdata.json')

from rest_framework.authtoken.models import Token
@pytest.fixture
def get_or_create_token(db, create_user):
   user = create_user()
   token, _ = Token.objects.get_or_create(user=user)
   return token
   
# Test for 401 Unauthorized Error when no Token is present
from django.urls import reverse
@pytest.mark.django_db
def test_unauthed_request(api_client, get_or_create_token):
   url = reverse('Random')
   response = api_client.get(url)
   assert response.status_code == 401

# Test that Random gets some data and returns properly
from django.urls import reverse
@pytest.mark.django_db
def test_random_request(api_client, get_or_create_token):
   url = reverse('Random')
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.get(url)
   assert response.status_code == 200

# Test that CardSet gets 10 Cards
@pytest.mark.django_db
def test_cardset_request(api_client, get_or_create_token):
   url = reverse('CardSet')
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.get(url)
   assert len(response.data) == 10
   
# Test that Card/[id] gets the correct stuff
@pytest.mark.django_db
def test_specific_card_request(api_client, get_or_create_token):
   should_be = {'id': 1791, 'uuid': 'ad13d548-c718-4d05-9439-e44d64feae12', 'card_name': 'Black Market', 'set_num': 0, 'set_name': 'Promo', 'type': 'Action', 'cost': '$3', 'card_text': '+$2\\nReveal the top 3 cards of the Black Market deck. You may buy one of them immediately. Put the unbought cards on the bottom of the Black Market deck in any order.\\d(Before the game, make a Black Market deck out of one copy of each Kingdom card not in '}
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.get('/cards/1791/')
   print(response.data)
   assert response.data == should_be