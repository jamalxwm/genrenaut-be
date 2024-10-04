import pytest
import responses
from django.test import TransactionTestCase
from django.db import IntegrityError
from django.core.management import call_command
from genrenaut.genres.utils import fetch_everynoise_genres, populate_genres
from genrenaut.genres.models import Genre

@pytest.mark.django_db(transaction=True)
class TestGenreUtils(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('migrate')

    def setUp(self):
        Genre.objects.all().delete()

    def test_populate_genres_success(self):
        genre_list = [('Pop', 'playlist123'), ('Rock', 'playlist124')]
        populate_genres(genre_list)
        assert Genre.objects.count() == 2
        assert Genre.objects.filter(name='Pop').exists()
        assert Genre.objects.filter(name='Rock').exists()

    def test_populate_genres_integrity_error(self):
        Genre.objects.create(name='Pop', spotify_playlist_id='playlist123')
        with pytest.raises(IntegrityError):
            populate_genres([('Pop', 'playlist123')])
        assert Genre.objects.count() == 1

@responses.activate
def test_fetch_genres_success():
    # Mock the HTTP response
    responses.add(responses.GET, 'http://example.com',
                  body='<table class="tracks"><span class="note"><a href="spotify:playlist:123">Rock</a></span></table>',
                  status=200)
    
    # Call the function
    result = fetch_everynoise_genres('http://example.com')
    
    # Check the result
    assert result == [('Rock', '123')]

@responses.activate
def test_fetch_genres_http_error():
    # Mock an unsuccessful HTTP response
    responses.add(responses.GET, 'http://example.com', status=404)
    
    # Test that an HTTP error is raised
    with pytest.raises(Exception):
        fetch_everynoise_genres('http://example.com')