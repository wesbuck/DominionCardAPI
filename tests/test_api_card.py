import uuid
import pytest
from django.urls import reverse
from django.core.management import call_command
from rest_framework.authtoken.models import Token

### Fixtures ###

@pytest.fixture
def api_client():
   from rest_framework.test import APIClient
   return APIClient()

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

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'tests/test_data.json')

@pytest.fixture
def get_or_create_token(db, create_user):
   user = create_user()
   token, _ = Token.objects.get_or_create(user=user)
   return token

@pytest.fixture
def all_card_fields():
   return ['id', 'uuid', 'card_name', 'set_name', 'type', 'is_kingdom_card', 'cost', 'card_text', 'source']

@pytest.fixture
def editable_card_fields():
   return ['card_name', 'set_name', 'type', 'cost', 'card_text']

@pytest.fixture
def test_card():
   return {'card_name': 'Test Card', 'set_name': 'Promo', 'type': 'Action', 'is_kingdom_card': 1, 'cost': '$3', 'card_text': 'Sample Card Text'}

@pytest.fixture
def updated_card():
   return {'card_name': 'Patched Card', 'set_name': 'Base', 'type': 'Deploy', 'is_kingdom_card': 0, 'cost': '$2', 'card_text': 'Updated Card Text'}

### GET ###

# Test for 401 Unauthorized Error when no Token is present
@pytest.mark.django_db
def test_unauthed_request(api_client):
   url = reverse('Random')
   response = api_client.get(url)
   assert response.status_code == 401

# Test for 200 response when accessing root
@pytest.mark.django_db
def test_root_request(api_client, get_or_create_token):
   url = ''
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.get(url)
   assert response.status_code == 200
   assert 'https://documenter.getpostman.com/view/' in response.data['Documentation']

# Test that Random gets some data and returns properly
@pytest.mark.django_db
def test_random_request(api_client, get_or_create_token, all_card_fields):
   url = reverse('Random')
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.get(url)
   assert response.status_code == 200
   for x in all_card_fields:
      assert x in response.data

# Test that Kingdom gets a single card and returns properly
@pytest.mark.django_db
def test_kingdom_request(api_client, get_or_create_token, all_card_fields):
   url = reverse('Kingdom')
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.get(url)
   assert response.status_code == 200
   for x in all_card_fields:
      assert x in response.data

# Test that CardSet gets 10 Cards
@pytest.mark.django_db
def test_cardset_request(api_client, get_or_create_token, all_card_fields):
   url = reverse('CardSet')
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.get(url)
   assert response.status_code == 200
   assert len(response.data) == 10
   for i in range(10):
      for x in all_card_fields:
         assert x in response.data[i]

# Test that All gets all Cards
@pytest.mark.django_db
def test_all_request(api_client, get_or_create_token, all_card_fields):
   url = reverse('All')
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.get(url)
   assert response.status_code == 200
   for x in all_card_fields:
      assert x in response.data[1]

# Test that Card/[id] gets the correct stuff
@pytest.mark.django_db
def test_specific_card_request(api_client, get_or_create_token, all_card_fields):
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.get('/cards/2/')
   assert response.status_code == 200
   assert response.data['source'] == 'default'
   for x in all_card_fields:
      assert x in response.data

### POST ###

# Test that POST card works
@pytest.mark.django_db
def test_card_creation_basic(api_client, get_or_create_token, test_card, editable_card_fields, all_card_fields):
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.post('/cards/', test_card)
   assert response.status_code == 201
   assert len(response.data) == len(all_card_fields)
   for x in editable_card_fields:
      assert response.data[x] == test_card[x]

# Test that POST card disallows duplicate card names
@pytest.mark.django_db
def test_card_creation_dup_name(api_client, get_or_create_token, test_card):
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   api_client.post('/cards/', test_card)
   response = api_client.post('/cards/', test_card)
   assert response.status_code == 400
   assert 'The card name already exists' in response.data['card_name']

# Test that POST card disallows setting id
@pytest.mark.django_db
def test_card_creation_cannot_set_id(api_client, get_or_create_token):
   test_card = {'id': '8221', 'card_name': 'Test Card 2', 'set_name': 'Promo', 'type': 'Action', 'cost': '$3', 'card_text': 'Sample Card Text'}
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.post('/cards/', test_card)
   assert response.status_code == 201
   assert response.data['id'] != test_card['id']
   assert isinstance(response.data['id'], int) 

# Test that POST card disallows setting uuid
@pytest.mark.django_db
def test_card_creation_cannot_set_uuid(api_client, get_or_create_token):
   test_card = {'uuid': '82f9bcc1-9ab9-4856-b04f-aace09668e21', 'card_name': 'Test Card 2', 'set_name': 'Promo', 'type': 'Action', 'cost': '$3', 'card_text': 'Sample Card Text'}
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.post('/cards/', test_card)
   assert response.status_code == 201
   assert response.data['uuid'] != test_card['uuid']
   assert len(response.data['uuid']) == 36

# Test that POST card disallows setting source
@pytest.mark.django_db
def test_card_creation_cannot_set_source(api_client, get_or_create_token):
   test_card = {'card_name': 'Test Card 2', 'set_name': 'Promo', 'type': 'Action', 'cost': '$3', 'card_text': 'Sample Card Text', 'source': 'Custom Source'}
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.post('/cards/', test_card)
   assert response.status_code == 201
   assert response.data['source'] != test_card['source']
   assert response.data['source'] == 'upload'

# Test that POST card requires required fields
@pytest.mark.django_db
def test_card_creation_required(api_client, get_or_create_token, editable_card_fields):
   test_card = {'is_kingdom_card': 1}
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.post('/cards/', test_card)
   assert response.status_code == 400
   for x in editable_card_fields:
      assert 'This field is required.' in response.data[x]

# Test that POST card auto-assigns uuid
@pytest.mark.django_db
def test_card_creation_assign_uuid(api_client, get_or_create_token, test_card):
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.post('/cards/', test_card)
   assert response.status_code == 201
   assert len(response.data['uuid']) == 36

# Test that Card/[id] can GET after POST
@pytest.mark.django_db
def test_get_created_card(api_client, get_or_create_token, test_card, editable_card_fields, all_card_fields):
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   new_card = api_client.post('/cards/', test_card)
   response = api_client.get('/cards/' + str(new_card.data['id']) + '/')
   assert response.status_code == 200
   assert len(response.data) == len(all_card_fields)
   for x in editable_card_fields:
      assert response.data[x] == test_card[x]

### DELETE ###

# Test that Card/[id] can DELETE after POST
@pytest.mark.django_db
def test_delete_created_card(api_client, get_or_create_token, test_card):
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   new_card = api_client.post('/cards/', test_card)
   response = api_client.delete('/cards/' + str(new_card.data['id']) + '/')
   assert response.status_code == 204

# Ensure 'csv' source cannot be deleted
@pytest.mark.django_db
def test_delete_protected_card(api_client, get_or_create_token):
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.delete('/cards/2/')
   assert response.status_code == 400
   assert 'Only manually created cards can be deleted.' in response.data

### PATCH ###

# Test that Card/[id] can PATCH after POST
@pytest.mark.django_db
def test_patch_created_card(api_client, get_or_create_token, test_card, updated_card, editable_card_fields):
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   new_card = api_client.post('/cards/', test_card)
   response = api_client.patch('/cards/' + str(new_card.data['id']) + '/', updated_card)
   assert response.status_code == 200
   for x in editable_card_fields:
      assert response.data[x] == updated_card[x]

# Ensure 'csv' source cannot be patched
@pytest.mark.django_db
def test_patch_protected_card(api_client, get_or_create_token, updated_card):
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.patch('/cards/2/', updated_card)
   assert response.status_code == 400
   assert 'Only manually created cards can be updated.' in response.data

### PUT ###

# Test that Card/[id] can PUT after POST
@pytest.mark.django_db
def test_put_created_card(api_client, get_or_create_token, test_card, updated_card, editable_card_fields):
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   new_card = api_client.post('/cards/', test_card)
   response = api_client.put('/cards/' + str(new_card.data['id']) + '/', updated_card)
   assert response.status_code == 200
   for x in editable_card_fields:
      assert response.data[x] == updated_card[x]

# Ensure 'csv' source cannot be updated
@pytest.mark.django_db
def test_put_protected_card(api_client, get_or_create_token, updated_card):
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.put('/cards/2/', updated_card)
   assert response.status_code == 400
   assert 'Only manually created cards can be updated.' in response.data
