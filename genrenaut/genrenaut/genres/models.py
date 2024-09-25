from django.db import models

class Genre(models.Model):
    display_name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    spotify_playlist_id = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name
