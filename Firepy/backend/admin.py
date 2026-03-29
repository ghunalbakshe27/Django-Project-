from django.contrib import admin
from django import forms
from .models import customuser, Song, RecentlyPlayed, LikedSong, Playlist

# Register simple models
admin.site.register(customuser)
admin.site.register(RecentlyPlayed)
admin.site.register(LikedSong)


# 🔥 Custom Multiple File Input Widget
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


# 🔥 Custom Form for Bulk Song Upload
class BulkSongUploadForm(forms.ModelForm):
    # Multiple file upload fields - FIXED
    audio_files = MultipleFileField(
        label='Audio Files (Select up to 10)',
        required=False,
        help_text='Select multiple MP3/audio files at once'
    )
    
    cover_images = MultipleFileField(
        label='Cover Images (Optional - Select up to 10)',
        required=False,
        help_text='Select cover images matching audio files order'
    )
    
    # Bulk fields for all songs
    artists = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter artists separated by newline\nArtist 1\nArtist 2\nArtist 3'}),
        required=False,
        help_text='One artist per line (same order as audio files)'
    )
    
    albums = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter albums separated by newline (optional)\nAlbum 1\nAlbum 2\nAlbum 3'}),
        required=False,
        help_text='One album per line (optional)'
    )
    
    durations = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter durations separated by newline (optional)\n3:45\n4:20\n5:00'}),
        required=False,
        help_text='One duration per line (optional, format: MM:SS)'
    )
    
    class Meta:
        model = Song
        fields = ['playlist', 'audio_files', 'cover_images', 'artists', 'albums', 'durations']


# 🔥 Custom Admin for Song with Bulk Upload + Bulk Actions
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    form = BulkSongUploadForm
    
    list_display = ['title', 'artist', 'album', 'playlist', 'duration', 'created_at']
    list_filter = ['playlist', 'created_at']
    search_fields = ['title', 'artist', 'album']
    ordering = ['-created_at']
    list_per_page = 50
    
    # 🆕 Bulk actions for playlist assignment
    actions = ['assign_to_playlist1', 'assign_to_playlist2', 'assign_to_artists', 'assign_to_top_charts']
    
    # Customize the form layout
    fieldsets = (
        ('🎵 Bulk Upload (Multiple Songs)', {
            'fields': ('playlist', 'audio_files', 'cover_images', 'artists', 'albums', 'durations'),
            'description': 'Upload multiple songs at once. File names will be used as song titles.'
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Check if bulk upload is being used
        audio_files = request.FILES.getlist('audio_files')
        
        if audio_files and len(audio_files) > 0:
            # Bulk upload mode
            self.bulk_create_songs(request, form, audio_files)
        else:
            # Single song upload
            super().save_model(request, obj, form, change)
    
    def bulk_create_songs(self, request, form, audio_files):
        """Handle bulk song creation"""
        from django.contrib import messages
        
        playlist = form.cleaned_data['playlist']
        cover_images = request.FILES.getlist('cover_images')
        
        # Parse text fields
        artists = [a.strip() for a in form.cleaned_data.get('artists', '').split('\n') if a.strip()]
        albums = [a.strip() for a in form.cleaned_data.get('albums', '').split('\n') if a.strip()]
        durations = [d.strip() for d in form.cleaned_data.get('durations', '').split('\n') if d.strip()]
        
        created_count = 0
        
        for i, audio_file in enumerate(audio_files[:10]):  # Limit to 10 songs
            # Extract title from filename (remove extension)
            title = audio_file.name.rsplit('.', 1)[0]
            
            # Get corresponding data
            artist = artists[i] if i < len(artists) else 'Unknown Artist'
            album = albums[i] if i < len(albums) else ''
            duration = durations[i] if i < len(durations) else ''
            cover_image = cover_images[i] if i < len(cover_images) else None
            
            # Create song
            Song.objects.create(
                title=title,
                artist=artist,
                album=album,
                playlist=playlist,
                audio_file=audio_file,
                cover_image=cover_image,
                duration=duration
            )
            created_count += 1
        
        messages.success(request, f'✅ Successfully created {created_count} songs in "{playlist.name}" playlist!')
    
    # 🆕 Bulk Action: Assign to Playlist-1
    @admin.action(description='📋 Assign selected songs to Playlist-1')
    def assign_to_playlist1(self, request, queryset):
        playlist = Playlist.objects.filter(playlist_type='playlist1').first()
        if playlist:
            updated = queryset.update(playlist=playlist)
            self.message_user(request, f'✅ {updated} songs assigned to {playlist.name}')
        else:
            self.message_user(request, '❌ No Playlist-1 found!', level='error')
    
    # 🆕 Bulk Action: Assign to Playlist-2
    @admin.action(description='📋 Assign selected songs to Playlist-2')
    def assign_to_playlist2(self, request, queryset):
        playlist = Playlist.objects.filter(playlist_type='playlist2').first()
        if playlist:
            updated = queryset.update(playlist=playlist)
            self.message_user(request, f'✅ {updated} songs assigned to {playlist.name}')
        else:
            self.message_user(request, '❌ No Playlist-2 found!', level='error')
    
    # 🆕 Bulk Action: Assign to Artists
    @admin.action(description='🎤 Assign selected songs to Artists')
    def assign_to_artists(self, request, queryset):
        playlist = Playlist.objects.filter(playlist_type='artists').first()
        if playlist:
            updated = queryset.update(playlist=playlist)
            self.message_user(request, f'✅ {updated} songs assigned to {playlist.name}')
        else:
            self.message_user(request, '❌ No Artists playlist found!', level='error')
    
    # 🆕 Bulk Action: Assign to Top Charts
    @admin.action(description='📊 Assign selected songs to Top Charts')
    def assign_to_top_charts(self, request, queryset):
        playlist = Playlist.objects.filter(playlist_type='top_charts').first()
        if playlist:
            updated = queryset.update(playlist=playlist)
            self.message_user(request, f'✅ {updated} songs assigned to {playlist.name}')
        else:
            self.message_user(request, '❌ No Top Charts playlist found!', level='error')


# 🔥 Custom Admin for Playlist
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'playlist_type', 'get_song_count', 'order', 'is_active', 'created_at']
    list_filter = ['playlist_type', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'cover_image')
        }),
        ('Classification', {
            'fields': ('playlist_type', 'order', 'is_active')
        }),
    )
    
    def get_song_count(self, obj):
        return obj.get_song_count()
    get_song_count.short_description = 'Songs'


# Customize admin site header
admin.site.site_header = '🔥 FIREPY Music Admin'
admin.site.site_title = 'FIREPY Admin'
admin.site.index_title = 'Welcome to FIREPY Administration'