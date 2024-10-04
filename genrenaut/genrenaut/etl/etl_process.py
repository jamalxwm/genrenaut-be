from django.utils.text import slugify
from genres.utils import fetch_everynoise_genres, fetch_musicalyst_genres, scrape_genre_description
from genres.models import Genre
# from genrenaut.songs.models import Song

def run_etl_process():
    everynoise_genres = fetch_everynoise_genres()
    musicalyst_genres = fetch_musicalyst_genres()
    
    # Create a dictionary of Musicalyst genres for easy lookup
    musicalyst_dict = {slugify(g['name']): g for g in musicalyst_genres}
    
    for genre in everynoise_genres:
        slug = slugify(genre['name'])
        musicalyst_data = musicalyst_dict.get(slug)
        
        if musicalyst_data:
            genre_obj, created = Genre.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': genre['name'],
                    'spotify_playlist_id': genre['spotify_playlist_id'],
                    'musicalyst_id': musicalyst_data['musicalyst_id']
                }
            )
            
            # Create or update the associated song
            if genre['spotify_song_id']:
                Song.objects.update_or_create(
                    spotify_id=genre['spotify_song_id'],
                    defaults={
                        'genre': genre_obj
                    }
                )
    
    # Add any remaining Musicalyst genres not found in Every Noise
    for genre in musicalyst_genres:
        slug = slugify(genre['name'])
        if not Genre.objects.filter(slug=slug).exists():
            Genre.objects.create(
                name=genre['name'],
                slug=slug,
                musicalyst_id=genre['musicalyst_id']
            )

def update_genre_descriptions():
    for genre in Genre.objects.filter(description__isnull=True):
        description = scrape_genre_description(genre.slug)
        if description:
            genre.description = description
            genre.save()