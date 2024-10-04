import pytest
import requests
import responses
from pytest_mock import MockerFixture
from django.test import TestCase
from django.db import IntegrityError
from django.core.management import call_command
from genrenaut.genres.utils import fetch_everynoise_genres, fetch_musicalyst_genres, scrape_genre_description
from genrenaut.genres.models import Genre

# Successfully fetches and parses the HTML from the given URL
@pytest.mark.django_db
def test_fetch_and_parse_html_success(mocker):
    # Mock the requests.get call to return a predefined HTML response
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '''
    <html>
        <body>
            <table class="tracks">
                <tr>
                    <td class="play song" trackid="ABC123">
                        <span class="note">
                            <a href="spotify:playlist:123">Genre1</a>
                        </span>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    '''
    mocker.patch('requests.get', return_value=mock_response)

    # Call the function
    genres = fetch_everynoise_genres()

    # Assert the expected output
    assert genres == [{'name': 'Genre1', 'spotify_playlist_id': '123', 'spotify_track_id': 'ABC123'}]

def test_handle_missing_elements_in_html(mocker):
    # Mock the requests.get call to return a predefined HTML response with missing elements
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '''
    <html>
        <body>
            <table class="tracks">
                <tr>
                    <td><span class="note"></span></td>
                </tr>
            </table>
        </body>
    </html>
    '''
    mocker.patch('requests.get', return_value=mock_response)

    # Call the function
    genres = fetch_everynoise_genres()

    # Assert the expected output is an empty list since no valid links are present
    assert genres == []


# Manages network failures or timeouts gracefully
def test_manage_network_failures(mocker):
    # Mock the requests.get call to simulate a network failure
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException
    mocker.patch('requests.get', return_value=mock_response)

    # Call the function and expect it to handle the network failure gracefully
    genres = fetch_everynoise_genres()
    
    # Assert that the function returns an empty list when a network error occurs
    assert genres == []

# Successfully fetches genres from the Musicalyst website
@pytest.mark.django_db
def test_fetch_genres_success(mocker):
    # Mock the requests.get call to return a predefined HTML response
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '''
    <html>
        <body>
            <ul>
                <li><a id="1">Rock</a></li>
                <li><a id="2">Jazz</a></li>
            </ul>
        </body>
    </html>
    '''
    mocker.patch('requests.get', return_value=mock_response)

    # Call the function
    genres = fetch_musicalyst_genres()

    # Assert the expected output
    assert genres == [
        {'name': 'Rock', 'musicalyst_id': '1'},
        {'name': 'Jazz', 'musicalyst_id': '2'}
    ]

def test_fetch_genres_failure(mocker):
    # Mock the requests.get call to simulate a network failure
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException
    mocker.patch('requests.get', return_value=mock_response)

    # Call the function and expect it to handle the network failure gracefully
    genres = fetch_musicalyst_genres()
    
    # Assert that the function returns an empty list when a network error occurs
    assert genres == []

@pytest.mark.django_db
def test_retrieves_genre_description_successfully(mocker):
    # Mock the requests.get call to return a predefined HTML response
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '''
    <html>
        <body>
            <p>This is a <a href="link">genre</a> description.</p>
        </body>
    </html>
    '''
    mocker.patch('requests.get', return_value=mock_response)

    # Call the function
    description = scrape_genre_description('valid-genre')

    # Assert the expected output
    assert description == 'This is a <a href="link">genre</a> description.'

def test_scrape_description_failure(mocker):
    # Mock the requests.get call to simulate a network failure
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException
    mocker.patch('requests.get', return_value=mock_response)

    # Call the function and expect it to handle the network failure gracefully
    description = scrape_genre_description('valid-genre')
    
    # Assert that the function returns an empty list when a network error occurs
    assert description == None