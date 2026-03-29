from django.core.management.base import BaseCommand
from django.core.files import File
from backend.models import Song, Playlist 
import os
import random
from pathlib import Path

class Command(BaseCommand):
    help = 'Bulk import songs from a folder with cover images'

    def add_arguments(self, parser):
        parser.add_argument(
            'folder_path',
            type=str,
            help='Path to the folder containing songs and images'
        )
        parser.add_argument(
            '--playlist',
            type=str,
            help='Playlist slug (e.g., top-hits, unassigned)',
            default=None
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Maximum number of songs to upload',
            default=None
        )
        parser.add_argument(
            '--random',
            action='store_true',
            help='Upload songs in random order (default: alphabetical order)'
        )

    def handle(self, *args, **options):
        folder_path = options['folder_path']
        
        if not os.path.exists(folder_path):
            self.stdout.write(self.style.ERROR(f'❌ Folder not found: {folder_path}'))
            return

        # 🆕 Get playlist from user
        playlist_slug = options['playlist']
        
        if not playlist_slug:
            # Show available playlists
            self.stdout.write(self.style.SUCCESS('\n📋 Available Playlists:'))
            playlists = Playlist.objects.all()
            for i, pl in enumerate(playlists, 1):
                self.stdout.write(f"  {i}. {pl.name} (slug: {pl.slug}) - {pl.get_playlist_type_display()}")
            
            # Ask user to choose
            self.stdout.write(self.style.WARNING('\n💡 Enter playlist slug (or press Enter for "unassigned"):'))
            playlist_slug = input('➡️  ').strip() or 'unassigned'
        
        # Get or create the playlist
        try:
            target_playlist = Playlist.objects.get(slug=playlist_slug)
            self.stdout.write(self.style.SUCCESS(f'✓ Using playlist: {target_playlist.name}'))
        except Playlist.DoesNotExist:
            if playlist_slug == 'unassigned':
                target_playlist = Playlist.objects.create(
                    slug='unassigned',
                    name='Unassigned Songs',
                    description='Songs imported but not assigned to any playlist yet',
                    playlist_type='playlist1',
                    order=9999,
                    is_active=True
                )
                self.stdout.write(self.style.SUCCESS('✓ Created "Unassigned" playlist'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ Playlist "{playlist_slug}" not found!'))
                return

        # 🆕 Get limit from user
        upload_limit = options['limit']
        
        if not upload_limit:
            self.stdout.write(self.style.WARNING('\n💡 How many songs to upload? (press Enter for ALL):'))
            limit_input = input('➡️  ').strip()
            upload_limit = int(limit_input) if limit_input.isdigit() else None

        # Supported formats
        audio_extensions = ('.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg')
        image_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.jfif', '.avif')
        
        uploaded_count = 0
        skipped_count = 0
        images_found = 0
        
        # 🔥 Get all files and sort them
        all_files = os.listdir(folder_path)
        
        # 🔥 Sort alphabetically (A-Z) or shuffle randomly
        if options['random']:
            random.shuffle(all_files)
            self.stdout.write(self.style.WARNING('🎲 Random upload mode enabled'))
        else:
            all_files.sort()  # Alphabetical order: A, B, C...
            self.stdout.write(self.style.SUCCESS('🔤 Alphabetical upload mode (A-Z)'))
        
        # Scan folder for audio files
        for filename in all_files:
            # 🆕 Check if limit reached
            if upload_limit and uploaded_count >= upload_limit:
                self.stdout.write(self.style.WARNING(f'\n⚠️  Upload limit reached: {upload_limit} songs'))
                break
            
            if filename.lower().endswith(audio_extensions):
                filepath = os.path.join(folder_path, filename)
                
                # 🔥 Extract artist and title from filename
                # Format: "Artist Name - Song Title.mp3"
                filename_without_ext = Path(filename).stem
                
                # Split by " - " (space-dash-space)
                if ' - ' in filename_without_ext:
                    parts = filename_without_ext.split(' - ', 1)  # Split only on first occurrence
                    artist_name = parts[0].strip()
                    song_title = parts[1].strip()
                else:
                    # If no separator found, use whole name as title
                    artist_name = 'Unknown'
                    song_title = filename_without_ext.strip()
                
                # Check if song already exists (check by both title and artist to avoid duplicates)
                if Song.objects.filter(title=song_title, artist=artist_name).exists():
                    self.stdout.write(self.style.WARNING(f'⚠️  Skipped (already exists): {artist_name} - {song_title}'))
                    skipped_count += 1
                    continue
                
                try:
                    # 🔥 Look for matching cover image using the same filename pattern
                    cover_image_file = None
                    for img_ext in image_extensions:
                        # Try exact match first: "Artist Name - Song Title.jpg"
                        img_path = os.path.join(folder_path, f"{filename_without_ext}{img_ext}")
                        if os.path.exists(img_path):
                            cover_image_file = img_path
                            break
                    
                    # Open and upload the audio file
                    with open(filepath, 'rb') as audio_file:
                        song = Song.objects.create(
                            title=song_title,
                            artist=artist_name,
                            playlist=target_playlist,
                            audio_file=File(audio_file, name=filename)
                        )
                        
                        # Upload cover image if found
                        if cover_image_file:
                            with open(cover_image_file, 'rb') as img_file:
                                song.cover_image.save(
                                    os.path.basename(cover_image_file),
                                    File(img_file),
                                    save=True
                                )
                            images_found += 1
                            self.stdout.write(self.style.SUCCESS(f'✓ {artist_name} - {song_title} (with image)'))
                        else:
                            self.stdout.write(self.style.SUCCESS(f'✓ {artist_name} - {song_title} (no image)'))
                    
                    uploaded_count += 1
                
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'❌ Error uploading {filename}: {str(e)}'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS(f'\n{"="*50}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total songs uploaded: {uploaded_count}'))
        self.stdout.write(self.style.SUCCESS(f'🖼️  Songs with images: {images_found}'))
        self.stdout.write(self.style.WARNING(f'⚠️  Total skipped: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS(f'📋 Playlist: {target_playlist.name}'))
        self.stdout.write(self.style.SUCCESS(f'{"="*50}\n'))