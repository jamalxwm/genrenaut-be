import requests
from bs4 import BeautifulSoup
from django.db import IntegrityError
from django.utils.text import slugify
# from genrenaut.genres.models import Genre

def fetch_everynoise_genres(url):
    # Send a GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the response
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table with class 'tracks'
        tracks_table = soup.find('table', class_='tracks')
        
        # Initialize an empty list to store genre information
        genres = []
        
        # Iterate through all span elements with class 'note' in the tracks table
        for note_span in tracks_table.find_all('span', class_='note'):
            # Find the anchor tag within the span
            link = note_span.find('a')
            
            # Check if the link exists and has an 'href' attribute
            if link and 'href' in link.attrs:
                href = link['href']
                
                # Check if the href starts with 'spotify:playlist:'
                if href.startswith('spotify:playlist:'):
                    # Extract the playlist ID from the href
                    playlist_id = href.split(':')[-1]
                    
                    # Get the genre name from the link text
                    genre_name = link.text.strip()
                    
                    # Append a tuple of (genre_name, playlist_id) to the genres list
                    genres.append((genre_name, playlist_id))
        
        # Return the list of genres
        return genres
    else:
        # If the request was not successful, raise an HTTP error
        response.raise_for_status()

def populate_genres(genre_list):
    for name, playlist_id in genre_list:
        slug = slugify(name)
        Genre.objects.create(name=name, spotify_playlist_id=playlist_id, slug=slug)
    print(f"Successfully added {len(genre_list)} genres.")

# url="https://everynoise.com/thesoundofeverything.html"
# genres = fetch_everynoise_genres(url)
# populate_genres(genres)

def fetch_musicalyst_genres(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        genres = []
        
        # Find all 'li' elements with 'a' tags inside
        for li in soup.find_all('li'):
            a_tag = li.find('a')
            if a_tag and 'id' in a_tag.attrs:
                genre_name = a_tag.text.strip()
                genre_id = a_tag['id']
                genres.append((genre_name, genre_id))
        
        return genres
    else:
        response.raise_for_status()

# Example usage:
# url = "https://musicalyst.com/genres"
# genres = fetch_musicalyst_genres(url)
# print(genres)

def scrape_genre_description(genre_slug):
    url = f"https://musicalyst.com/genre/{genre_slug}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.text, 'html.parser')
        description_p = soup.find('p')
        
        if description_p:
            # Convert the p tag to a string, preserving internal HTML
            description = str(description_p)
            return description
        else:
            return f"No description found for genre: {genre_name}"
    
    except requests.RequestException as e:
        return f"Error fetching description for {genre_name}: {str(e)}"
    
# Example usage:
description = scrape_genre_description("ambient-industrial")
print(description)