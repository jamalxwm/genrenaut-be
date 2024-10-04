import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify
import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify

def fetch_everynoise_genres(url):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    tracks_table = soup.find('table', class_='tracks')
    
    genres = []
    for note_span in tracks_table.find_all('span', class_='note'):
        link = note_span.find('a')
        if link and 'href' in link.attrs:
            href = link['href']
            if href.startswith('spotify:playlist:'):
                playlist_id = href.split(':')[-1]
                genre_name = link.text.strip()
                # Extract song ID (assuming it's in a specific format)
                song_id = None  # You'll need to implement this based on the actual HTML structure
                genres.append({
                    'name': genre_name,
                    'spotify_playlist_id': playlist_id,
                    'spotify_song_id': song_id
                })
    
    return genres

def fetch_musicalyst_genres(url):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    genres = []
    for li in soup.find_all('li'):
        a_tag = li.find('a')
        if a_tag and 'id' in a_tag.attrs:
            genre_name = a_tag.text.strip()
            genre_id = a_tag['id']
            genres.append({
                'name': genre_name,
                'musicalyst_id': genre_id
            })
    
    return genres

def scrape_genre_description(genre_slug):
    url = f"https://musicalyst.com/genre/{genre_slug}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        description_p = soup.find('p')
        
        if description_p:
            description = ''.join(str(content) if content.name == 'a' else content.strip() for content in description_p.contents)
            return description.strip()
        else:
            return None
    
    except requests.RequestException:
        return None