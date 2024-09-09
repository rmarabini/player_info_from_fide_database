# FIDE Ratings Scripts

This repository contains two Python scripts to download, store, and query FIDE chess player ratings from the FIDE database. The first script downloads and processes a list of FIDE players, storing the information in the local file. The second script queries the file and outputs player records based on input FIDE IDs.

## Table of Contents

* Requirements
* Installation
  * Usage
    1. FIDE Ratings Download and Storage Script
    1. Query FIDE Records and Output to CSV
  * Example Usage
 
## Requirements

To run these scripts, you need Python 3 and the following Python libraries:

    * sqlite3 (part of the Python standard library)
    * urllib (for downloading the FIDE files)
    * xml (for XML parsing)
    * tabulate (for pretty printing the output on the terminal)
    * argparse (for handling command-line arguments)

You will also need to install sqlite3 


## Installation
In the following instalation commands are provided for windows, linux and mac users vaery likely have already all the software needed.

Install python (install typing in a terminal ``` winget install python3```)  and sqlite3 ((type in a erminal ``` winget install sqlite.sqlite ```). From this repository download the files fide_download.py and fide_query.py and all the python modules that are not installed by default. Very likely the only one missing is __tabulate__
Open a terminal (__cmd__)  and type:

```
pip install tabulate
```
### Usage

#### FIDE Ratings Download and Storage Script

This script downloads the players_list_xml.zip file from the FIDE website and preprocess it. Execute it from a terminal (__cmd__) as (in the terminal you must be in the same directory in which you downloaded the scripts):

```
python fide_download.py
```
or alternativelly just double click it.  Depending on your computer and conectivity this step may take one or two minutes. Remember that FIDE updates this databases monthly.

The player information includes fields such as fide_id, name, country, sex, title, rating, and others.
No command-line options are required for this script, as it automatically downloads and processes the FIDE data.

#### Query FIDE Records and Output to CSV

This script takes a file with FIDE IDs (one per line), retrieves the corresponding records from the downloaded information, and outputs the results to a CSV file. The results are also displayed on the console.

```
python fide_query.py <input_file> <output_file.csv> --fields <fields> --database <database>
```

###### Arguments:

*    input_file: A file containing FIDE IDs, one per line.
*    output_file.csv: The CSV file where the results will be saved.
*    --fields: (Optional) A space-separated list of fields to include in the output. Default fields are fide_id, name, country, and rating.
*    --database: (Optional) The SQLite database file. The default is fide_ratings.db.

###### Available Fields:

*    fide_id: The player's unique FIDE ID.
*    name: The player's name.
*    country: The player's country.
*    sex: The player's gender.
*    title: The player's chess title (if any).
*    rating: The player's standard FIDE rating.
*    games_played: The number of standard games played.
*    rapid_rating: The player's rapid FIDE rating.
*    rapid_games: The number of rapid games played.
*    blitz_rating: The player's blitz FIDE rating.
*    blitz_games: The number of blitz games played.
*    birthday: The player's birth year.

###### Example:

```
python fide_query.py fide_ids.txt output.csv --fields fide_id name country rating blitz_rating
```

## Example Usage

### FIDE Ratings Download and Storage Script

To download and store the FIDE ratings data in a local file:

```
python fide_download.py
```

### Query FIDE Records and Output to CSV

Suppose you have a file called fide_ids.txt containing the following FIDE IDs:

```
22226141
32066171
22298851
```

To query the database for these FIDE IDs and output specific fields (fide_id, name, country, rating) to both the terminal and a CSV file (from a terminal (__cmd__) execute):

```
python fide_query.py fide_ids.txt output.csv --fields fide_id name country rating
```

The output will look like this in the terminal:


```
FIDE Records:

+----------+--------------------------+---------+--------+
| fide_id  |           name           | country | rating |
+----------+--------------------------+---------+--------+
| 22226141 | Martinez Fernandez, Raul |   ESP   |  2149  |
| 22298851 |  Hernandez Ramos, David  |   ESP   |  2101  |
| 32066171 |  Gomez Carreno, Martin   |   ESP   |  2124  |
+----------+--------------------------+---------+--------+
```


And the same results will be saved in output.csv as follows:

```
fide_id,name,country,rating
22226141,"Martinez Fernandez, Raul",ESP,2149
22298851,"Hernandez Ramos, David",ESP,2101
32066171,"Gomez Carreno, Martin",ESP,2124
```

this file may be read from excel or similar programs.

