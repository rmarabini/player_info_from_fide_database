import zipfile
import urllib.request
import os
import sqlite3
import xml.etree.ElementTree as ET

# Function to retrieve the zip file from the FIDE website
def retrieve_file(file_name):
    print(f"Downloading {file_name}...")
    try:
        urllib.request.urlretrieve(f"http://ratings.fide.com/download/{file_name}", file_name)
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
        name = player.find('name').text.strip()  # Remove any leading/trailing whitespace
        country = player.find('country').text
        sex = player.find('sex').text
        title = player.find('title').text if player.find('title') is not None else None
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
    return conn

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
    INSERT OR REPLACE INTO fide_ratings(fide_id, name, country, sex, title, rating, games_played, rapid_rating, rapid_games, blitz_rating, blitz_games, birthday)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    try:
        c = conn.cursor()
        c.execute("PRAGMA synchronous = OFF")
        c.executemany(sql, players)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Main function to orchestrate the downloading, parsing, and saving of FIDE ratings
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
        unzip(file_name)
        
        # Check if the XML file exists and parse it
        if os.path.exists(xml_file_name):
            players = parse_xml(xml_file_name)

            # Insert or update records in the database
            if players:
                insert_or_update_fide_ratings(conn, players)
                print(f"Inserted or updated {len(players)} records from {xml_file_name} into the database.")
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

