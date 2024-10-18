# /*
#  * Copyright (c) 2024 R.Marabini
#  * 
#  * This program is free software: you can redistribute it and/or modify
#  * it under the terms of the GNU General Public License as published by
#  * the Free Software Foundation, version 3.
#  *
#  * This program is distributed in the hope that it will be useful, but
#  * WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  * General Public License for more details.
#  *
#  * You should have received a copy of the GNU General Public License
#  * along with this program. If not, see <http://www.gnu.org/licenses/>.
#  */

import zipfile
import urllib.request
import os
import sqlite3
import xml.etree.ElementTree as ET
import hashlib


HASH_FILE_NAME = "last_hash.txt"


# Function to compute the hash of a file
def compute_file_hash(file_name):
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_name, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                hash_sha256.update(data)
        return hash_sha256.hexdigest()
    except FileNotFoundError:
        return None


# Function to retrieve the zip file from the FIDE website
def retrieve_file(file_name):
    print(f"Downloading {file_name}...")
    try:
        urllib.request.urlretrieve(f"https://ratings.fide.com/download/{file_name}", file_name)
        print(f"Retrieved {file_name} successfully.")
        return True
    except Exception as e:
        print(f"Failed to retrieve {file_name}: {e}")
        return False


# Function to unzip the file
def unzip(file_name):
    print(f"Unzipping {file_name}...")
    try:
        with zipfile.ZipFile(file_name, 'r') as z:
            z.extractall(".")  # Extract the XML file(s) to the current directory
        os.remove(file_name)
        print(f"Removed {file_name}")
    except Exception as e:
        print(f"Failed to unzip {file_name}: {e}")


# Function to parse the XML and extract player data
def parse_xml(file_name):
    print(f"Parsing XML: {file_name}")
    tree = ET.parse(file_name)
    root = tree.getroot()

    players = []

    # Extract player data based on XML structure
    for player in root.findall('player'):
        fide_id = player.find('fideid').text
        # Remove any leading/trailing whitespace
        name = player.find('name').text.strip()
        country = player.find('country').text
        sex = player.find('sex').text
        title = player.find('title').text\
            if player.find('title') is not None else None
        rating = int(player.find('rating').text)
        games = int(player.find('games').text)
        rapid_rating = int(player.find('rapid_rating').text)
        rapid_games = int(player.find('rapid_games').text)
        blitz_rating = int(player.find('blitz_rating').text)
        blitz_games = int(player.find('blitz_games').text)
        birthday = player.find('birthday').text

        players.append((fide_id, name, country, sex, title, rating, games, rapid_rating, rapid_games, blitz_rating, blitz_games, birthday))

    return players


# Function to connect to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None


# Function to create the table for storing FIDE ratings
def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS fide_ratings (
        fide_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        country TEXT NOT NULL,
        sex TEXT NOT NULL,
        title TEXT,
        rating INTEGER NOT NULL,
        games_played INTEGER NOT NULL,
        rapid_rating INTEGER,
        rapid_games INTEGER,
        blitz_rating INTEGER,
        blitz_games INTEGER,
        birthday TEXT
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


# Function to insert or update player data into the database
def insert_or_update_fide_ratings(conn, players):
    sql = '''
    INSERT INTO fide_ratings(
        fide_id,
        name,
        country,
        sex,
        title,
        rating,
        games_played,
        rapid_rating,
        rapid_games,
        blitz_rating,
        blitz_games,
        birthday)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    try:
        c = conn.cursor()
        c.execute("PRAGMA synchronous = OFF")
        c.executemany(sql, players)
        conn.commit()
    except sqlite3.Error as e:
        print(e)


# Function to save the hash of the last file
def save_last_hash(hash_value):
    with open(HASH_FILE_NAME, "w") as f:
        f.write(hash_value)


# Function to load the last saved hash
def load_last_hash():
    if os.path.exists(HASH_FILE_NAME):
        with open(HASH_FILE_NAME, "r") as f:
            return f.read().strip()
    return None


# Function to delete all records from the FIDE ratings table
def delete_all_records(conn):
    try:
        sql = 'DELETE FROM fide_ratings'
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        print("cleaning all records from the old table.")
    except sqlite3.Error as e:
        print(f"Error deleting records: {e}")


# Main function to orchestrate the downloading, parsing, and saving of 
# FIDE ratings
def main():
    # Specify the database file name
    database = "fide_ratings.db"
    file_name = "players_list_xml.zip"
    xml_file_name = "players_list_xml_foa.xml"

    # Create a connection to the database
    conn = create_connection(database)

    # Create the FIDE ratings table if it doesn't exist
    if conn:
        create_table(conn)

    # Download, unzip, and parse the XML file
    if retrieve_file(file_name):
        # Compute the hash of the newly downloaded file
        new_file_hash = compute_file_hash(file_name)

        # Load the previous file's hash
        previous_file_hash = load_last_hash()

        # Check if the file has changed
        if new_file_hash == previous_file_hash:
            print("File has not changed. No need to update the database.")
        else:
            print("New file detected. Updating the database...")
            unzip(file_name)
            
            # Check if the XML file exists and parse it
            if os.path.exists(xml_file_name):
                players = parse_xml(xml_file_name)

                # Delete all records from the database before inserting new data
                delete_all_records(conn)
                
                # Insert or update records in the database
                if players:
                    insert_or_update_fide_ratings(conn, players)
                    print(f"Inserted {len(players)} records from {xml_file_name} into the database.")
                    
                    # Save the hash of the new file
                    save_last_hash(new_file_hash)
                else:
                    print(f"No players found in {xml_file_name}")

                # Optionally remove the XML file after processing
                os.remove(xml_file_name)
            else:
                print(f"Failed to find {xml_file_name}")

    # Close the database connection
    if conn:
        conn.close()


if __name__ == "__main__":
    main()
