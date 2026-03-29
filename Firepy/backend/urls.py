from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='root'),
    
    # Homepage & Main Pages
    path('homepage/', views.homepage, name='homepage'),
    path('aboutus/', views.aboutus, name='aboutus'),    
    # 🔥 NEW: Dynamic Playlist Route (must be after specific routes)
    path('playlist/<slug:slug>/', views.playlist_view, name='playlist_view'),
    
     # Homepage Search (🔥 NEW: Dedicated Search Endpoint)
    path('api/search/', views.search_songs, name='search_songs'),
    
    # Authentication
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='ogregister'),
    path('logout/', views.user_logout, name='user_logout'),
    
    # API Endpoints
    path('api/personal-details/', views.get_personal_details, name='get_personal_details'),
    path('api/recent-history/', views.get_recent_history, name='get_recent_history'),
    path('api/liked-songs/', views.get_liked_songs, name='get_liked_songs'),
    # 🔥 NEW: Rename Liked Songs Playlist
    path('api/rename-liked-playlist/', views.rename_liked_playlist, name='rename_liked_playlist'),


    path('api/like-song/<int:song_id>/', views.toggle_like_song, name='toggle_like_song'),
    path('api/track-play/<int:song_id>/', views.track_song_play, name='track_song_play'),

    #email testing
    path('test-email/', views.test_email, name='test_email'),  # Test URL

    # Search API
    path('api/search-songs/', views.search_songs_in_playlist, name='search_songs'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)