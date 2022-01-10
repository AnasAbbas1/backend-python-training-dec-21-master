from datetime import datetime
import pytest

from libwishlist import Context, domain

def test_create_wishlist(client):
    response = client.post(
        '/wishlist/create',
        headers = {'x-forwarded-user': 'nizar'},
        json={
            "name": "trip",
            "items": ["sunscreen", "hat"]
        }
    )
    wishlist_nr = response.json()['wishlist_nr']
    
    assert wishlist_nr

def test_get_wishlist(client):
    response = client.get(
        '/wishlist/WL123456C',
    )

    assert response.json()['wishlist_nr']['name'] == 'dummy'


def test_delete_wishlist(client):
    response = client.post(
        '/wishlist/trip',
    )
    assert response.json() == ['success']