<div align="center">

<!-- Animated Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=🔥%20FIREPY&fontSize=80&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Where%20Music%20Meets%20Fire&descAlignY=60&descSize=22" width="100%"/>

<!-- Typing Animation -->
<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=700&size=22&pause=1000&color=FF6B35&center=true&vCenter=true&width=600&lines=🎵+Stream+Music+Like+Never+Before;🔥+Built+with+Django+%2B+MySQL;🎨+Glassmorphism+UI+Design;🚀+Full-Stack+Music+Platform" alt="Typing SVG" />
</a>

<br/>

<!-- Badges Row 1 -->
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"/>
<img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white"/>
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/>
<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
<img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>

<br/>

<!-- Badges Row 2 -->
<img src="https://img.shields.io/badge/SendGrid-1A82E2?style=for-the-badge&logo=sendgrid&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-FF6B35?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Status-Active%20Dev-00FF88?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Platform-Web-9B59B6?style=for-the-badge"/>

</div>

---

<div align="center">

## 🔥 What is FIREPY?

</div>

> **FIREPY** is a full-stack music streaming web platform built on **Django + MySQL**, designed for music lovers who want more than just a playlist. With a deep purple glassmorphism UI, live search, audio streaming, liked songs, recently played history, and artist profiles — FIREPY delivers a premium experience without the premium price tag.

---

<div align="center">

## ✨ Features

</div>

<table>
<tr>
<td width="50%">

### 🎵 Music
- 🎧 **Song Streaming** — Full audio playback with controls
- 🔍 **Live Search** — Debounced real-time song/artist search
- ❤️ **Liked Songs** — Save and manage your favorites
- 🕓 **Recently Played** — Auto-tracked listening history
- 📋 **Queue System** — Mini player with queue support

</td>
<td width="50%">

### 👤 User
- 🔐 **Auth System** — Register, Login, Logout
- ✉️ **SendGrid Emails** — Welcome emails on signup
- 🎨 **Custom Playlists** — Rename your liked playlist
- 📱 **Mobile Ready** — Responsive bottom-sheet UI
- 🎭 **Artist Profiles** — Dedicated artist pages

</td>
</tr>
</table>

---

<div align="center">

## 🏗️ Project Structure

</div>

```
🔥 Firepy/
│
├── 📁 firepy/                  ← Django project config
│   ├── ⚙️  settings.py
│   ├── 🌐 urls.py
│   ├── 🚀 asgi.py / wsgi.py
│   └── 🔧 __init__.py
│
├── 📁 backend/                 ← Main app
│   ├── 🧠 models.py            ← Song, Artist, LikedSong, RecentlyPlayed
│   ├── 👁️  views.py            ← API endpoints + page views
│   ├── 🛣️  urls.py             ← URL routing
│   ├── 🔑 admin.py
│   │
│   ├── 📁 templates/           ← HTML pages
│   │   ├── 🏠 homepage.html
│   │   ├── 🎵 generes.html
│   │   ├── 🎤 arjit.html
│   │   ├── 🎶 phonk.html
│   │   ├── 🥁 punjabi hits.html
│   │   └── ... (13 more pages)
│   │
│   └── 📁 migrations/
│
├── 🧪 manage.py
└── 📖 README.md
```

---

<div align="center">

## ⚡ Quick Start

</div>

### 1️⃣ Clone the Repo

```bash
git clone <repository-url>
cd Firepy
```

### 2️⃣ Set Up Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install django mysqlclient sendgrid
```

### 4️⃣ Configure Settings

```python
# firepy/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'firepy_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 5️⃣ Run Migrations & Start Server

```bash
python manage.py migrate
python manage.py runserver
```

🚀 Open **http://127.0.0.1:8000** and enjoy the fire!

---

<div align="center">

## 🧰 Tech Stack

</div>

<div align="center">

| Layer | Technology |
|-------|-----------|
| 🖥️ **Backend** | Django 4.x (Python) |
| 🗄️ **Database** | MySQL |
| 🎨 **Frontend** | HTML5, CSS3 (Glassmorphism), Vanilla JS |
| 📧 **Email** | SendGrid API |
| 🎵 **Audio** | HTML5 `<audio>` API |
| 🔍 **Search** | Debounced Fetch API |
| 📱 **Mobile UI** | Responsive CSS, Bottom-Sheet Modal |

</div>

---

<div align="center">

## 📡 API Endpoints

</div>

```
GET  /api/search-songs/         → Live search by title/artist
POST /api/like-song/            → Like or unlike a song
GET  /api/liked-songs/          → Get user's liked songs
GET  /api/recently-played/      → Get listening history
POST /api/recently-played/add/  → Log a played song
```

---

<div align="center">

## 🤝 Contributing

Contributions are welcome! Let's build something 🔥 together.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

</div>

---

<div align="center">

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<!-- Footer Wave -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=twinkling" width="100%"/>

**Made with 🔥 and ☕ by a passionate developer**

*"Music is the shorthand of emotion."*

</div>
