from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class customuser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name']

    def __str__(self):
        return self.username


# 🔥 NEW: Playlist Model
class Playlist(models.Model):
    PLAYLIST_TYPE_CHOICES = [
        ('playlist1', 'PlayList-1'),
        ('playlist2', 'The New Wave'),
        ('artists', 'Artists'),
        ('top_charts', 'The Top Charts'),
        ('New_section', 'Industry Pulse'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='playlist_covers/', blank=True, null=True)
    playlist_type = models.CharField(max_length=50, choices=PLAYLIST_TYPE_CHOICES, default='playlist1')
    slug = models.SlugField(unique=True, help_text="URL-friendly name (e.g., 'top-hits')")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_playlist_type_display()})"
    
    def get_song_count(self):
        return self.songs.count()


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200, blank=True, null=True)
    cover_image = models.ImageField(upload_to='song_covers/', blank=True, null=True)
    audio_file = models.FileField(upload_to='songs/', blank=True, null=True)
    
    # 🔥 TEMPORARY: Make playlist nullable for migration
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='songs')
    
    duration = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.artist}"


# 🔥 Track Recently Played Songs
class RecentlyPlayed(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE, related_name='recently_played')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    played_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-played_at']
        unique_together = ['user', 'song']
    
    def __str__(self):
        return f"{self.user.username} - {self.song.title}"


# 🔥 Track Liked Songs
class LikedSong(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE, related_name='liked_songs')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-liked_at']
        unique_together = ['user', 'song']
    
    def __str__(self):
        return f"{self.user.username} likes {self.song.title}"
    
# 🔥 NEW: User's Custom Playlist Name
class UserLikedPlaylistName(models.Model):
    user = models.OneToOneField(customuser, on_delete=models.CASCADE, related_name='liked_playlist_name')
    playlist_name = models.CharField(max_length=100, default='My Liked Songs')
    last_updated = models.DateTimeField(default=timezone.now)
    
    def can_rename(self):
        return True
    
    def days_until_rename(self):
        return 0
    
    def __str__(self):
        return f"{self.user.username}'s playlist: {self.playlist_name}"