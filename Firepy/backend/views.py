from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from backend.models import Song, customuser, RecentlyPlayed, LikedSong, Playlist, UserLikedPlaylistName
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.utils import timezone
from backend.utils import send_welcome_email
from django.db.models import Q
import json
import random
from datetime import datetime, timedelta
from django.utils import timezone

from firepy import settings

User = customuser

def search_songs(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'songs': []})
    
    songs = Song.objects.filter(
        Q(title__icontains=query) | Q(artist__icontains=query)
    ).values('id', 'title', 'artist', 'audio_file', 'cover_image')[:20]
    
    results = []
    seen = set()  # 🔥 track kar lo kaun se songs already add ho gaye
    
    for song in songs:
        # Title + Artist combination unique key banao
        key = (song['title'].lower().strip(), song['artist'].lower().strip())
        
        if key in seen:
            continue  # duplicate hai — skip karo
        seen.add(key)  # pehli baar aa rha hai — mark karo
        
        audio_url = ''
        cover_url = ''
        
        if song['audio_file']:
            audio_url = request.build_absolute_uri(
                settings.MEDIA_URL + song['audio_file']
            )
        if song['cover_image']:
            cover_url = request.build_absolute_uri(
                settings.MEDIA_URL + song['cover_image']
            )
        
        results.append({
            'id': song['id'],
            'title': song['title'],
            'artist': song['artist'],
            'audio_url': audio_url,
            'cover_url': cover_url,
        })
    
    return JsonResponse({'songs': results})

@require_GET
def search_songs_in_playlist(request):
    q = request.GET.get('q', '').strip()
    playlist_id = request.GET.get('playlist_id', '')

    # If search term is empty, return empty list
    if not q:
        return JsonResponse({'songs': []})

    # Base queryset: songs in this playlist only
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        songs_qs = playlist.songs.all()  # assumes ManyToMany or FK — adjust if needed
    except Playlist.DoesNotExist:
        return JsonResponse({'songs': [], 'error': 'Playlist not found'})

    # icontains = case-insensitive "contains" search
    # We search in both title AND artist fields using OR (|)
    from django.db.models import Q
    results = songs_qs.filter(
        Q(title__icontains=q) | Q(artist__icontains=q)
    )[:10]  # limit to 10 results max

    songs_data = [
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '',
        }
        for song in results
    ]

    return JsonResponse({'songs': songs_data})




# 🔥 Personal Details API
@login_required(login_url='user_login')
def get_personal_details(request):
    user = request.user
    data = {
        'full_name': user.get_full_name() or user.username,
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined.strftime('%B %d, %Y')
    }
    return JsonResponse(data)


# 🔥 Recent History API
@login_required(login_url='user_login')
def get_recent_history(request):
    recent_songs = RecentlyPlayed.objects.filter(user=request.user).select_related('song')[:20]
    
    data = {
        'songs': [
            {
                'id': item.song.id,
                'title': item.song.title,
                'artist': item.song.artist,
                'cover': item.song.cover_image.url if item.song.cover_image else '/static/backend/images/default-cover.jpg',
                'played_at': item.played_at.strftime('%B %d, %Y'),
                'duration': item.song.duration or '0:00'
            }
            for item in recent_songs
        ]
    }
    return JsonResponse(data)

@login_required(login_url='user_login')
def get_liked_songs(request):
    liked_songs = LikedSong.objects.filter(user=request.user).select_related('song')
    
    # Get or create user's playlist name
    playlist_name_obj, created = UserLikedPlaylistName.objects.get_or_create(
        user=request.user,
        defaults={'playlist_name': 'My Liked Songs'}
    )
    
    data = {
        'playlist_name': playlist_name_obj.playlist_name,
        'can_rename': playlist_name_obj.can_rename(),
        'days_until_rename': playlist_name_obj.days_until_rename(),
        'songs': [
            {
                'id': item.song.id,
                'title': item.song.title,
                'artist': item.song.artist,
                'cover': item.song.cover_image.url if item.song.cover_image else '/static/backend/images/default-cover.jpg',
                'audio': item.song.audio_file.url if item.song.audio_file else '',  # 🔥 Audio URL
                'liked_at': item.liked_at.strftime('%B %d, %Y'),
                'duration': '  '  # 🔥 Add duration if available
            }
            for item in liked_songs
        ]
    }
    return JsonResponse(data)


# 🔥 NEW: Rename Liked Playlist
@login_required(login_url='user_login')
def rename_liked_playlist(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_name = data.get('playlist_name', '').strip()

            if not new_name:
                return JsonResponse({'status': 'error', 'message': 'Playlist name cannot be empty'}, status=400)

            if len(new_name) > 100:
                return JsonResponse({'status': 'error', 'message': 'Name too long (max 100 characters)'}, status=400)

            playlist_name_obj, created = UserLikedPlaylistName.objects.update_or_create(
                user=request.user,
                defaults={
                    'playlist_name': new_name,
                    'last_updated': timezone.now()
                }
            )

            if not created:
                playlist_name_obj.playlist_name = new_name
                playlist_name_obj.last_updated = timezone.now()
                playlist_name_obj.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Playlist renamed successfully!',
                'playlist_name': new_name,
                'can_rename': True,   # ✅ always true now
                'days_until_rename': 0
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# 🔥 Toggle Like Song
@login_required(login_url='user_login')
def toggle_like_song(request, song_id):
    if request.method == 'POST':
        try:
            song = Song.objects.get(id=song_id)
            liked_song, created = LikedSong.objects.get_or_create(user=request.user, song=song)
            
            if not created:
                liked_song.delete()
                return JsonResponse({'status': 'unliked', 'message': 'Song removed from liked songs'})
            else:
                return JsonResponse({'status': 'liked', 'message': 'Song added to liked songs'})
        except Song.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Song not found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# 🔥 Track Song Play
@login_required(login_url='user_login')
def track_song_play(request, song_id):
    if request.method == 'POST':
        try:
            song = Song.objects.get(id=song_id)
            recent, created = RecentlyPlayed.objects.update_or_create(
                user=request.user,
                song=song,
                defaults={'played_at': timezone.now()}
            )
            return JsonResponse({'status': 'success', 'message': 'Play tracked'})
        except Song.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Song not found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# 🔥 UPDATED: Homepage with Dynamic Playlists

def homepage(request):
    user = request.user
    
    # Check if user is authenticated
    if user.is_authenticated:
        # Get full name
        full_name = f"{user.first_name} {user.last_name}".strip()
        if not full_name:
            full_name = user.username
        
        username = full_name
        email = user.email
        is_authenticated = True
    else:
        # For anonymous users
        username = "Firepy Guest"
        email = "Guest@firepy.com"
        is_authenticated = False
    
    # 🔥 Get playlists dynamically grouped by type
    playlists_by_type = {
        'playlist1': Playlist.objects.filter(playlist_type='playlist1', is_active=True).order_by('order'),
        'playlist2': Playlist.objects.filter(playlist_type='playlist2', is_active=True).order_by('order'),
        'artists': Playlist.objects.filter(playlist_type='artists', is_active=True).order_by('order'),
        'top_charts': Playlist.objects.filter(playlist_type='top_charts', is_active=True).order_by('order'),
        'New_section': Playlist.objects.filter(playlist_type='New_section', is_active=True).order_by('order'),
    }
    
    context = {
        'username': username,
        'email': email,
        'is_authenticated': is_authenticated,
        'playlists_by_type': playlists_by_type,
        'user_count': User.objects.count(),
    }
    return render(request, 'backend/homepage.html', context)


# 🔥 UPDATED: About Us
def aboutus(request):
    return render(request, 'backend/aboutus.html')


# 🔥 NEW: Generic Playlist View
def playlist_view(request, slug):
    """Generic view for any playlist by slug"""
    
    # Check if user is authenticated
    if not request.user.is_authenticated:
        # For non-authenticated users, show limited view with login prompt
        playlist = get_object_or_404(Playlist, slug=slug, is_active=True)
        context = {
            'playlist': playlist,
            'is_authenticated': False,
            'requires_login': True
        }
        return render(request, 'backend/playlist_player.html', context)
    
    # For authenticated users, show full playlist
    playlist = get_object_or_404(Playlist, slug=slug, is_active=True)
    songs = playlist.songs.all().order_by('created_at')[:50]
    
    songs_json = json.dumps([
        {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'cover': song.cover_image.url if song.cover_image else '/static/backend/images/default-cover.jpg',
            'audio': song.audio_file.url if song.audio_file else '',
            'duration': song.duration or '0:00'
        }
        for song in songs
    ])
    
    context = {
        'playlist': playlist,
        'songs': songs,
        'songs_json': songs_json,
        'is_authenticated': True,
        'requires_login': False
    }
    return render(request, 'backend/playlist_player.html', context)

# 🔥 AUTHENTICATION VIEWS
@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'backend/index.html')


@csrf_protect
def user_register(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        
        # Split fullname
        name_parts = fullname.strip().split(' ', 1)
        first_name = name_parts[0] if name_parts else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Validation
        if not fullname.strip():
            messages.error(request, 'Full name is required!')
            return redirect('ogregister')
            
        if password != confirm_password:
            messages.error(request, 'Passwords does not match!')
            return redirect('ogregister')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('ogregister')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('ogregister')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_password(password)
            user.save()

            # 🔥 SEND WELCOME EMAIL
            send_welcome_email(email, fullname or username)
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('user_login')
            
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('ogregister')
    
    return render(request, 'backend/ogregister.html')


def user_logout(request):
    logout(request)
    messages.success(request, '')
    return redirect('homepage')

def test_email(request):
    """
    Test function to check if email is working
    URL: http://127.0.0.1:8000/test-email/
    """
    success = send_welcome_email('test@example.com', 'Test User')
    if success:
        return JsonResponse({'status': 'success', 'message': 'Test email sent!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Email failed!'})
    
# 🔥 Forgot Password — email lo, OTP bhejo
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
            return render(request, 'backend/forgot_password.html')

        # OTP generate karo
        otp = str(random.randint(100000, 999999))
        expiry = (timezone.now() + timedelta(minutes=10)).isoformat()

        # Session mein store karo
        request.session['reset_otp'] = otp
        request.session['reset_otp_expiry'] = expiry
        request.session['reset_email'] = email

        # Email bhejo
        from backend.utils import send_otp_email
        send_otp_email(email, user.username, otp)

        messages.success(request, 'OTP sent to your registered email!')
        return redirect('verify_otp')

    return render(request, 'backend/forgot_password.html')


# 🔥 OTP Verify
def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        saved_otp = request.session.get('reset_otp')
        expiry_str = request.session.get('reset_otp_expiry')

        if not saved_otp or not expiry_str:
            messages.error(request, 'Session expired. Please try again.')
            return redirect('forgot_password')

        # Expiry check
        expiry = datetime.fromisoformat(expiry_str)
        if timezone.now() > expiry:
            messages.error(request, 'OTP expired. Please request a new one.')
            return redirect('forgot_password')

        if entered_otp == saved_otp:
            request.session['otp_verified'] = True
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'backend/verify_otp.html')


# 🔥 Reset Password
def reset_password(request):
    if not request.session.get('otp_verified'):
        messages.error(request, 'Please verify OTP first.')
        return redirect('forgot_password')

    if request.method == 'POST':
        new_pass = request.POST.get('new_password', '')
        confirm_pass = request.POST.get('confirm_password', '')

        if new_pass != confirm_pass:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'backend/reset_password.html')

        if len(new_pass) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'backend/reset_password.html')

        email = request.session.get('reset_email')
        try:
            user = User.objects.get(email=email)
            user.set_password(new_pass)
            user.save()

            # Session saaf karo
            for key in ['reset_otp', 'reset_otp_expiry', 'reset_email', 'otp_verified']:
                request.session.pop(key, None)

            messages.success(request, 'Password reset successful! Please login.')
            return redirect('user_login')

        except User.DoesNotExist:
            messages.error(request, 'Something went wrong. Try again.')

    return render(request, 'backend/reset_password.html')  


# 🔥 Change Username
@login_required(login_url='user_login')
def change_username(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_username = data.get('username', '').strip()

            if not new_username:
                return JsonResponse({'status': 'error', 'message': 'Username cannot be empty'})

            if len(new_username) < 3:
                return JsonResponse({'status': 'error', 'message': 'Username must be at least 3 characters'})

            if len(new_username) > 20:
                return JsonResponse({'status': 'error', 'message': 'Username max 20 characters allowed'})

            # Same username check
            if new_username == request.user.username:
                return JsonResponse({'status': 'error', 'message': 'This is already your username!'})

            # Unique check
            if User.objects.filter(username=new_username).exists():
                return JsonResponse({'status': 'error', 'message': 'Username already taken!'})

            # Save
            request.user.username = new_username
            request.user.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Username updated successfully!',
                'new_username': new_username
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})