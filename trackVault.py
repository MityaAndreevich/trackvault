import sqlite3
import csv
import xml.etree.ElementTree as ET
import os

# Connect to the database
conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# Create fresh tables
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title   TEXT UNIQUE,
    artist_id  INTEGER
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

def insert_track(name, artist, album, genre, length, rating, count):
    cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))
    cur.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
    artist_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (genre,))
    cur.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
    genre_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)', (album, artist_id))
    cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (name, album_id, genre_id, length, rating, count))

# Ask for file
fname = input("Enter file name (CSV or XML): ").strip()
if not fname:
    fname = 'tracks.csv'

if not os.path.exists(fname):
    print("❌ File not found.")
else:
    if fname.lower().endswith('.csv'):
        with open(fname, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                if len(row) < 9:
                    continue
                name, artist, album, genre = row[0], row[1], row[2], row[3]
                length, rating, count = row[5], row[7], row[8]
                if not (name and artist and album and genre):
                    continue
                print(f"CSV Inserting: {name} | {artist} | {album} | {genre}")
                insert_track(name, artist, album, genre, length, rating, count)

    elif fname.lower().endswith('.xml'):
        def lookup(d, key):
            found = False
            for child in d:
                if found:
                    return child.text
                if child.tag == 'key' and child.text == key:
                    found = True
            return None

        tree = ET.parse(fname)
        root = tree.getroot()

        for track in root.findall('dict/dict/dict'):
            name = lookup(track, 'Name')
            artist = lookup(track, 'Artist')
            album = lookup(track, 'Album')
            genre = lookup(track, 'Genre')
            length = lookup(track, 'Total Time')
            rating = lookup(track, 'Rating')
            count = lookup(track, 'Play Count')

            if not (name and artist and album and genre):
                continue
            print(f"XML Inserting: {name} | {artist} | {album} | {genre}")
            insert_track(name, artist, album, genre, length, rating, count)
    else:
        print("❌ Unsupported file type. Use .csv or .xml")

# Save and close
conn.commit()

# Export top tracks
export = input("\nDo you want to export top 10 tracks to CSV? (y/n): ").strip().lower()
if export == 'y':
    top_query = '''
    SELECT Track.title, Artist.name, Album.title, Genre.name 
    FROM Track 
    JOIN Genre ON Track.genre_id = Genre.id 
    JOIN Album ON Track.album_id = Album.id 
    JOIN Artist ON Album.artist_id = Artist.id 
    ORDER BY Artist.name 
    LIMIT 10
    '''
    top_results = cur.execute(top_query).fetchall()
    with open("top_tracks_export.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Track', 'Artist', 'Album', 'Genre'])
        writer.writerows(top_results)
    print("\n📤 Exported to top_tracks_export.csv")

conn.close()
print("\n✅ Done")
