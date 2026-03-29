# Firepy Project

Firepy is a Django-based web application designed to provide a platform for music enthusiasts. This project includes various features such as music genres, playlists, and artist information.

## Project Structure

The project is organized into the following directories and files:

```
Firepy
├── firepy
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── backend
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── templates
│   │   ├── index.html
│   │   ├── aboutus.html
│   │   ├── arjit.html
│   │   ├── bhajan.html
│   │   ├── drivelist.html
│   │   ├── generes.html
│   │   ├── homepage.html
│   │   ├── honeys.html
│   │   ├── indianhits.html
│   │   ├── mixlist.html
│   │   ├── new releases.html
│   │   ├── ogregister.html
│   │   ├── phonk.html
│   │   ├── punjabi hits.html
│   │   ├── subh1.html
│   │   ├── top.html
│   │   ├── topeng.html
│   │   └── trend.html
│   └── urls.py
├── manage.py
├── .vscode
│   └── settings.json
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Firepy
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install django
   ```

4. Run the migrations:
   ```
   python manage.py migrate
   ```

5. Start the development server:
   ```
   python manage.py runserver
   ```

## Features

- User registration and login
- Music genres and playlists
- Artist profiles
- Responsive design

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.