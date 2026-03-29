// ========== ACCOUNT SIDEBAR ==========
const accountBtn = document.getElementById("accountBtn");
const accountSidebar = document.getElementById("accountSidebar");
const overlay = document.getElementById("overlay");
const closeSidebar = document.getElementById("closeSidebar");

function openAccountSidebar() {
    accountSidebar.classList.add("show");
    overlay.classList.add("show");
    document.body.style.overflow = "hidden";
}

function closeAccountSidebar() {
    accountSidebar.classList.remove("show");
    overlay.classList.remove("show");
    document.body.style.overflow = "auto";
}

accountBtn.addEventListener("click", openAccountSidebar);
closeSidebar.addEventListener("click", closeAccountSidebar);
overlay.addEventListener("click", closeAccountSidebar);

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && accountSidebar.classList.contains("show")) {
        closeAccountSidebar();
    }
});


// ========== MODALS ==========
const personalModal = document.getElementById("personalModal");
const historyModal = document.getElementById("historyModal");
const likedModal = document.getElementById("likedModal");

const closePersonalModal = document.getElementById("closePersonalModal");
const closeHistoryModal = document.getElementById("closeHistoryModal");
const closeLikedModal = document.getElementById("closeLikedModal");

// Open Modal Function
function openModal(modal) {
    modal.classList.add("show");
    document.body.style.overflow = "hidden";
}

// Close Modal Function
function closeModal(modal) {
    modal.classList.remove("show");
    document.body.style.overflow = "auto";
}

// Close buttons
closePersonalModal.addEventListener("click", () => closeModal(personalModal));
closeHistoryModal.addEventListener("click", () => closeModal(historyModal));
closeLikedModal.addEventListener("click", () => {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentAudio = null;
    }
    closeModal(likedModal);
});

// // Close modal when clicking outside
// [personalModal, historyModal, likedModal].forEach(modal => {
//     modal.addEventListener("click", (e) => {
//         if (e.target === modal) {
//             closeModal(modal);
//         }
//     });
// });

// ESC key to close modals
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        closeModal(personalModal);
        closeModal(historyModal);
        if (currentAudio) {
            currentAudio.pause();
            currentAudio.currentTime = 0;
            currentAudio = null;
        }
        closeModal(likedModal);
    }
});


// ========== PERSONAL DETAILS ==========
document.getElementById("personalDetails").addEventListener("click", async () => {
    console.log("Personal Details clicked");
    closeAccountSidebar();
    openModal(personalModal);

    const content = document.getElementById("personalDetailsContent");
    content.innerHTML = '<div class="loading">Loading...</div>';

    try {
        const response = await fetch('/api/personal-details/');
        const data = await response.json();

        content.innerHTML = `
            <div class="detail-item">
                <div class="detail-label">Full Name</div>
                <div class="detail-value">${data.full_name}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Username</div>
                <div class="detail-value">@${data.username}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Email Address</div>
                <div class="detail-value">${data.email}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Member Since</div>
                <div class="detail-value">${data.date_joined}</div>
            </div>
        `;
    } catch (error) {
        console.error("Error fetching personal details:", error);
        content.innerHTML = '<div class="empty-state"><p>Failed to load personal details</p></div>';
    }
});


// ========== RECENT HISTORY - UPDATED ==========
document.getElementById("recentHistory").addEventListener("click", async () => {
    console.log("Recent History clicked");
    closeAccountSidebar();
    openModal(historyModal);

    const content = document.getElementById("historyContent");
    content.innerHTML = '<div class="loading">Loading...</div>';

    try {
        const response = await fetch('/api/recent-history/', {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        });
        const data = await response.json();

        if (data.songs.length === 0) {
            content.innerHTML = `
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="M12 6v6l4 2"/>
                    </svg>
                    <p>No songs played yet. Start listening to build your history!</p>
                </div>
            `;
            return;
        }

        const songsHTML = data.songs.map(song => `
            <div class="song-item">
                <img src="${song.cover}" alt="${song.title}" class="song-cover">
                <div class="song-info">
                    <div class="song-title">${song.title}</div>
                    <div class="song-artist">${song.artist}</div>
                </div>
                <div class="song-meta">
                    <span class="song-time">${song.played_at}</span>
                </div>
            </div>
        `).join('');

        content.innerHTML = `<div class="song-list">${songsHTML}</div>`;
    } catch (error) {
        console.error("Error fetching recent history:", error);
        content.innerHTML = '<div class="empty-state"><p>Failed to load recent history</p></div>';
    }
});


// ========== HELPER FUNCTIONS FOR SONG PAGES ==========

// Call this function when a song is played
async function trackSongPlay(songId) {
    try {
        const response = await fetch(`/api/track-play/${songId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        const data = await response.json();
        console.log('Song play tracked:', data);
    } catch (error) {
        console.error('Error tracking song play:', error);
    }
}

// Call this function when like button is clicked
async function toggleLikeSong(songId) {
    try {
        const response = await fetch(`/api/like-song/${songId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        const data = await response.json();
        console.log('Like toggled:', data);
        return data;
    } catch (error) {
        console.error('Error toggling like:', error);
    }
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Export functions for use in other pages
window.trackSongPlay = trackSongPlay;
window.toggleLikeSong = toggleLikeSong;

// ========== LIKED SONGS WITH AUDIO PLAYER ==========
let currentAudio = null;  // Track currently playing audio

document.getElementById("likedSongs").addEventListener("click", async () => {
    console.log("Liked Songs clicked");
    closeAccountSidebar();
    openModal(likedModal);

    const content = document.getElementById("likedContent");
    content.innerHTML = '<div class="loading">Loading...</div>';

    try {
        const response = await fetch('/api/liked-songs/', {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
            }
        });
        const data = await response.json();

        if (data.songs.length === 0) {
            content.innerHTML = `
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                    </svg>
                    <p>No liked songs yet. Start liking songs!</p>
                </div>
            `;
            return;
        }

        // Build HTML with play button and audio player
        const songsHTML = data.songs.map((song, index) => `
            <div class="song-item-playable" data-song-index="${index}">
                <img src="${song.cover}" alt="${song.title}" class="song-cover">
                <div class="song-info-full">
                    <div class="song-title">${song.title}</div>
                    <div class="song-artist">${song.artist}</div>
                    <div class="song-meta">
                        <span class="song-time">Liked ${song.liked_at}</span>
                        <span class="song-duration">${song.duration}</span>
                    </div>
                    
                    <!-- Play Button -->
                    <button class="play-song-btn" data-audio="${song.audio}" data-title="${song.title}" data-artist="${song.artist}">
                        ▶ Play
                    </button>
                    
                    <!-- Audio Player (Hidden Initially) -->
                    <div class="audio-player-container" style="display: none;">
                        <audio class="inline-audio-player" src="${song.audio}" preload="metadata"></audio>
                        <div class="audio-controls">
                            <button class="audio-play-pause">▶</button>
                            <div class="audio-progress-bar">
                                <div class="audio-progress"></div>
                            </div>
                            <span class="audio-time">0:00 / ${song.duration}</span>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        // Render content with playlist name and rename option
        content.innerHTML = `
            <div class="playlist-name-header">
                <h3 id="playlistNameDisplay">${data.playlist_name}</h3>
                <button class="rename-playlist-btn" id="renamePlaylistBtn" title="Rename Playlist" ${!data.can_rename ? 'disabled' : ''}>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                    </svg>
                </button>
                ${!data.can_rename ? `<span class="rename-timer">Rename in ${data.days_until_rename} day(s)</span>` : ''}
            </div>
            <div class="song-list-playable">${songsHTML}</div>
        `;

        // Attach event listeners
        attachPlayButtonListeners();
        attachRenameListener(data.can_rename);

    } catch (error) {
        console.error("Error fetching liked songs:", error);
        content.innerHTML = '<div class="empty-state"><p>Failed to load liked songs</p></div>';
    }
});


// 🔥 Attach Play Button Listeners
function attachPlayButtonListeners() {
    document.querySelectorAll('.play-song-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const audioSrc = this.getAttribute('data-audio');
            const title = this.getAttribute('data-title');
            const artist = this.getAttribute('data-artist');
            const container = this.nextElementSibling;
            const audio = container.querySelector('.inline-audio-player');

            // Stop currently playing audio
            if (currentAudio && currentAudio !== audio) {
                currentAudio.pause();
                currentAudio.currentTime = 0;
                currentAudio.closest('.audio-player-container').style.display = 'none';
                currentAudio.closest('.song-item-playable').querySelector('.play-song-btn').style.display = 'inline-block';
            }

            // Toggle current audio
            if (container.style.display === 'none') {
                container.style.display = 'block';
                this.style.display = 'none';
                audio.play();
                currentAudio = audio;

                // Setup audio controls
                setupAudioControls(container, audio);
            }
        });
    });
}


// 🔥 Setup Audio Controls
function setupAudioControls(container, audio) {
    const playPauseBtn = container.querySelector('.audio-play-pause');
    const progressBar = container.querySelector('.audio-progress-bar');
    const progress = container.querySelector('.audio-progress');
    const timeDisplay = container.querySelector('.audio-time');

    // Play/Pause
    playPauseBtn.addEventListener('click', () => {
        if (audio.paused) {
            audio.play();
            playPauseBtn.textContent = '⌷⌷';
        } else {
            audio.pause();
            playPauseBtn.textContent = '▶';
        }
    });

    // Progress bar update
    audio.addEventListener('timeupdate', () => {
        const percent = (audio.currentTime / audio.duration) * 100;
        progress.style.width = percent + '%';
        timeDisplay.textContent = `${formatTime(audio.currentTime)} / ${formatTime(audio.duration)}`;
    });

    // Seek functionality
    progressBar.addEventListener('click', (e) => {
        const rect = progressBar.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const width = rect.width;
        audio.currentTime = (clickX / width) * audio.duration;
    });

    // Auto play/pause button update
    audio.addEventListener('play', () => playPauseBtn.textContent = '⌷⌷');
    audio.addEventListener('pause', () => playPauseBtn.textContent = '▶');
}


// 🔥 Format Time Helper
function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
}


// 🔥 Attach Rename Listener
function attachRenameListener(canRename) {
    const renameBtn = document.getElementById('renamePlaylistBtn');
    if (!renameBtn) return;

    renameBtn.addEventListener('click', async function () {
        if (!canRename) {
            alert('You can only rename once every 2 days!');
            return;
        }

        const newName = prompt('Enter new playlist name:');
        if (!newName || !newName.trim()) return;

        try {
            const response = await fetch('/api/rename-liked-playlist/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ playlist_name: newName.trim() })
            });

            const data = await response.json();

            if (data.status === 'success') {
                document.getElementById('playlistNameDisplay').textContent = data.playlist_name;
                alert(data.message);
                renameBtn.disabled = true;
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error renaming playlist:', error);
            alert('Failed to rename playlist');
        }
    });
}


// New search functionality for homepage
/* ═══════════════════════════════════════
   FIREPY — Search + Mini Player Logic
   ═══════════════════════════════════════ */

(function () {
    // ── DOM refs ──
    const searchToggle = document.getElementById('searchToggle');
    const searchExpanded = document.getElementById('searchExpanded');
    const searchInput = document.getElementById('searchInput');
    const searchClose = document.getElementById('searchClose');
    const searchResults = document.getElementById('searchResults');

    const miniPlayer = document.getElementById('miniPlayer');
    const mpAudio = document.getElementById('mpAudio');
    const mpCover = document.getElementById('mpCover');
    const mpTitle = document.getElementById('mpTitle');
    const mpArtist = document.getElementById('mpArtist');
    const mpPlayPause = document.getElementById('mpPlayPause');
    const mpPlayIcon = document.getElementById('mpPlayIcon');
    const mpPauseIcon = document.getElementById('mpPauseIcon');
    const mpPrev = document.getElementById('mpPrev');
    const mpNext = document.getElementById('mpNext');
    const mpClose = document.getElementById('mpClose');
    const mpLikeBtn = document.getElementById('mpLikeBtn');
    const mpProgressBar = document.getElementById('mpProgressBar');
    const mpProgressFill = document.getElementById('mpProgressFill');
    const mpProgressThumb = document.getElementById('mpProgressThumb');
    const mpCurrentTime = document.getElementById('mpCurrentTime');
    const mpDuration = document.getElementById('mpDuration');

    // ── State ──
    let queue = [];          // current search results
    let currentIdx = -1;
    let debounceTimer = null;

    // ── Search: open/close ──
    searchToggle.addEventListener('click', () => {
        searchExpanded.classList.add('active');
        searchToggle.style.display = 'none';
        setTimeout(() => searchInput.focus(), 50);
    });

    function closeSearch() {
        searchExpanded.classList.remove('active');
        searchToggle.style.display = '';
        searchInput.value = '';
        searchResults.innerHTML = '';
    }

    searchClose.addEventListener('click', closeSearch);
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeSearch(); });
    document.addEventListener('click', e => {
        if (searchExpanded.classList.contains('active') &&
            !searchExpanded.contains(e.target) &&
            !searchToggle.contains(e.target)) {
            closeSearch();
        }
    });

    // ── Search: debounced input ──
    searchInput.addEventListener('input', function () {
        const q = this.value.trim();
        clearTimeout(debounceTimer);

        if (!q) { searchResults.innerHTML = ''; return; }

        searchResults.innerHTML = '<div class="search-loading">Searching...</div>';

        debounceTimer = setTimeout(() => fetchSongs(q), 280);
    });

    function fetchSongs(q) {
        fetch(`/api/search/?q=${encodeURIComponent(q)}`)
            .then(r => r.json())
            .then(data => renderResults(data.songs || []))
            .catch(() => {
                searchResults.innerHTML = '<div class="search-empty">Something went wrong.</div>';
            });
    }

    function renderResults(songs) {
        if (!songs.length) {
            searchResults.innerHTML = '<div class="search-empty">No songs found.</div>';
            return;
        }

        queue = songs;
        const defaultCover = '/static/backend/images/default-cover.jpg';

        searchResults.innerHTML = songs.map((song, i) => `
            <div class="search-result-item" data-idx="${i}">
                <img class="search-result-img"
                     src="${song.cover_url || defaultCover}"
                     alt="${song.title}"
                     onerror="this.src='${defaultCover}'">
                <div class="search-result-info">
                    <span class="search-result-title">${escHtml(song.title)}</span>
                    <span class="search-result-artist">${escHtml(song.artist || 'Unknown')}</span>
                </div>
                <div class="search-play-icon">
                    <svg viewBox="0 0 24 24"><polygon points="5,3 19,12 5,21"/></svg>
                </div>
            </div>
        `).join('');

        searchResults.querySelectorAll('.search-result-item').forEach(el => {
            el.addEventListener('click', () => {
                playSong(parseInt(el.dataset.idx));
                closeSearch();
            });
        });
    }

    // ── Player: play a song by index ──
    function playSong(idx) {
        if (idx < 0 || idx >= queue.length) return;
        currentIdx = idx;
        const song = queue[idx];
        const defaultCover = '/static/backend/images/default-cover.jpg';

        mpCover.src = song.cover_url || defaultCover;
        mpCover.onerror = () => { mpCover.src = defaultCover; };
        mpTitle.textContent = song.title;
        mpArtist.textContent = song.artist || 'Unknown';
        mpAudio.src = song.audio_url;
        mpAudio.play().catch(() => { });

        miniPlayer.classList.add('show');
        setPlayState(true);
        mpLikeBtn.classList.remove('liked');

        // Track play (agar tumhara endpoint hai toh)
        if (typeof trackSongPlay === 'function') trackSongPlay(song.id);
    }

    function setPlayState(playing) {
        if (playing) {
            mpPlayIcon.style.display = 'none';
            mpPauseIcon.style.display = '';
        } else {
            mpPlayIcon.style.display = '';
            mpPauseIcon.style.display = 'none';
        }
    }

    mpPlayPause.addEventListener('click', () => {
        if (mpAudio.paused) { mpAudio.play(); setPlayState(true); }
        else { mpAudio.pause(); setPlayState(false); }
    });

    mpPrev.addEventListener('click', () => { if (currentIdx > 0) playSong(currentIdx - 1); });
    mpNext.addEventListener('click', () => { if (currentIdx < queue.length - 1) playSong(currentIdx + 1); });
    mpAudio.addEventListener('ended', () => {
        if (currentIdx < queue.length - 1) playSong(currentIdx + 1);
        else setPlayState(false);
    });

    // ── Progress bar ──
    mpAudio.addEventListener('timeupdate', () => {
        if (!mpAudio.duration) return;
        const pct = (mpAudio.currentTime / mpAudio.duration) * 100;
        mpProgressFill.style.width = pct + '%';
        mpProgressThumb.style.left = pct + '%';
        mpCurrentTime.textContent = fmtTime(mpAudio.currentTime);
    });

    mpAudio.addEventListener('loadedmetadata', () => {
        mpDuration.textContent = fmtTime(mpAudio.duration);
    });

    mpProgressBar.addEventListener('click', e => {
        const rect = mpProgressBar.getBoundingClientRect();
        const pct = (e.clientX - rect.left) / rect.width;
        mpAudio.currentTime = pct * mpAudio.duration;
    });

    // ── Like button ──
    mpLikeBtn.addEventListener('click', () => {
        const song = queue[currentIdx];
        if (!song) return;
        mpLikeBtn.classList.toggle('liked');

        // Agar tumhara toggle_like_song endpoint hai:
        fetch(`/api/like-song/${song.id}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify({ song_id: song.id })
        }).catch(() => { });
    });

    // ── Close player ──
    mpClose.addEventListener('click', () => {
        mpAudio.pause();
        miniPlayer.classList.remove('show');
        setPlayState(false);
        currentIdx = -1;
    });

    // ── Helpers ──
    function fmtTime(s) {
        if (!s || isNaN(s)) return '0:00';
        const m = Math.floor(s / 60);
        const sec = Math.floor(s % 60).toString().padStart(2, '0');
        return `${m}:${sec}`;
    }

    function escHtml(str) {
        return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    function getCookie(name) {
        const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return v ? v.pop() : '';
    }

})();