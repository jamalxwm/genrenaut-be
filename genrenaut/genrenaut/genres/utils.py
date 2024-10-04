import requests
import logging
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify

def fetch_everynoise_genres():
    url = "https://everynoise.com/thesoundofeverything.html"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch genres from {url}: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    tracks_table = soup.find('table', class_='tracks')
    
    genres = []
    for row in tracks_table.find_all('tr'):
        # Extract track ID from the 'trackid' attribute of the 'td' element
        td = row.find('td', class_='play song')
        track_id = td['trackid'] if td and 'trackid' in td.attrs else None
        
        note_span = row.find('span', class_='note')
        if note_span:
            link = note_span.find('a')
            if link and 'href' in link.attrs:
                href = link['href']
                if href.startswith('spotify:playlist:'):
                    playlist_id = href.split(':')[-1]
                    genre_name = link.text.strip()
                    genres.append({
                        'name': genre_name,
                        'spotify_playlist_id': playlist_id,
                        'spotify_track_id': track_id
                    })
    
    return genres

def fetch_musicalyst_genres():
    url = "https://musicalyst.com/genres"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch genres from {url}: {e}")
        return []
    
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
            description = ''
            for content in description_p.contents:
                if content.name == 'a':
                    description += str(content)
                else:
                    description += content
            return description.strip()
        else:
            return None
    
    except requests.RequestException:
        return None
    
    