
import pytest
from django.urls import reverse
from django.core.management import call_command

@pytest.fixture
def api_client():
   from rest_framework.test import APIClient
   return APIClient()

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'tests/test_users.json')
 
@pytest.mark.django_db
@pytest.mark.parametrize(
   'username, password, status_code', [
       ('', '', 400),
       ('', 'adminpass', 400),
       ('user', '', 400),
       ('user', 'adminpass', 400),
       ('admin', 'invalid_pass', 400),
       ('admin', 'adminpass', 200),
   ]
)
def test_get_auth_token_requests(username, password, status_code, api_client):
   url = reverse('get_auth_token')
   data = {
       'username': username,
       'password': password
   }
   response = api_client.post(url, data=data)
   print(response.data)
   assert response.status_code == status_code