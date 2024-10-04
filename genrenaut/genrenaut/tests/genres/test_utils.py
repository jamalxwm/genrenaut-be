import pytest
import requests
from genrenaut.genres.utils import fetch_everynoise_genres, fetch_musicalyst_genres, scrape_genre_description

class TestFetchEverynoiseGenres:
    # Successfully fetches and parses the HTML from the given URL
    @pytest.mark.django_db
    def test_successful_fetch_and_parse(self, mocker):
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

    def test_handles_missing_elements(self, mocker):
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
    def test_handles_network_failures(self, mocker):
        # Mock the requests.get call to simulate a network failure
        mock_response = mocker.Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException
        mocker.patch('requests.get', return_value=mock_response)

        # Call the function and expect it to handle the network failure gracefully
        genres = fetch_everynoise_genres()
        
        # Assert that the function returns an empty list when a network error occurs
        assert genres == []

class TestFetchMusicalystGenres:
    # Successfully fetches genres from the Musicalyst website
    @pytest.mark.django_db
    def test_successful_fetch(self, mocker):
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

    def test_handles_network_failures(self, mocker):
        # Mock the requests.get call to simulate a network failure
        mock_response = mocker.Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException
        mocker.patch('requests.get', return_value=mock_response)

        # Call the function and expect it to handle the network failure gracefully
        genres = fetch_musicalyst_genres()
        
        # Assert that the function returns an empty list when a network error occurs
        assert genres == []

class TestScrapeGenreDescription:
    @pytest.mark.django_db
    def test_successful_retrieval(self, mocker):
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

    def test_handles_network_failures(self, mocker):
        # Mock the requests.get call to simulate a network failure
        mock_response = mocker.Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException
        mocker.patch('requests.get', return_value=mock_response)

        # Call the function and expect it to handle the network failure gracefully
        description = scrape_genre_description('valid-genre')
    
        # Assert that the function returns an empty list when a network error occurs
        assert description == None