<p align="center">
  <img src="trackvault-logo.png" width="200" alt="TrackVault logo" />
</p>

# 🎵 TrackVault (CSV/XML to SQLite)

**TrackVault** is a Python project that allows you to import music track data into a normalized SQLite database from either:

- A CSV file (`tracks.csv`) — from iTunes or similar export
- An XML file (`Library.xml`) — e.g., iTunes library export

It creates a structured database with separate tables for:
- Artist
- Album
- Genre
- Track

## Features

✅ Supports both CSV and XML input formats  
✅ Auto-creates normalized schema with foreign keys  
✅ Debug `print()` statements to trace inserted records  
✅ Handles missing or incomplete data gracefully  
✅ Can export query results to CSV after import  
✅ Automatically detects file type by extension  

---

## 📁 Files

- `trackvault.py` — main Python script
- `tracks.csv` — optional sample CSV file
- `Library.xml` — optional iTunes XML file
- `trackdb.sqlite` — generated output SQLite database
- `README.md` — this project documentation

---

## 💻 How to Run

```bash
python trackvault.py
```

When prompted:
- Enter `tracks.csv` — to import from CSV
- Enter `Library.xml` — to import from XML

Once finished, the program will offer to **export top tracks** to a new CSV file.

---

## 🧱 Database Schema

```
Artist(id INTEGER PRIMARY KEY, name TEXT UNIQUE)
Genre(id INTEGER PRIMARY KEY, name TEXT UNIQUE)
Album(id INTEGER PRIMARY KEY, title TEXT UNIQUE, artist_id INTEGER)
Track(id INTEGER PRIMARY KEY, title TEXT UNIQUE, album_id INTEGER,
      genre_id INTEGER, len INTEGER, rating INTEGER, count INTEGER)
```

---

## 🔍 Example Query

To view top tracks after import:
```sql
SELECT Track.title, Artist.name, Album.title, Genre.name 
FROM Track 
JOIN Genre ON Track.genre_id = Genre.id 
JOIN Album ON Track.album_id = Album.id 
JOIN Artist ON Album.artist_id = Artist.id 
ORDER BY Artist.name 
LIMIT 10;
```

---

## 📤 Export Feature

After importing, the script will ask if you'd like to **export the top 10 tracks** to a CSV file. 
This will generate a file called `top_tracks_export.csv`.

---

## 🚀 License
MIT or free to use for educational/personal projects.

---

## 📌 Ideas for Future Features
- GUI using Tkinter or PyQt
- Web interface with Flask
- API to upload files and trigger import
- Integration with music APIs (e.g. Last.fm, Spotify)
