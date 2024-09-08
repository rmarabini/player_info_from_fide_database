# FIDE Ratings Scripts

This repository contains two Python scripts to download, store, and query FIDE chess player ratings from the FIDE database. The first script downloads and processes a list of FIDE players, storing their information in an SQLite database. The second script queries the database and outputs player records based on input FIDE IDs.

#Table of Contents

* Requirements
* Installation
  * Usage
    1. FIDE Ratings Download and Storage Script
    1. Query FIDE Records and Output to CSV
  * Example Usage
 
## Requirements

To run these scripts, you need Python 3 (https://www.howtogeek.com/197947/how-to-install-python-on-windows/) and the following Python libraries:

    * sqlite3 (part of the Python standard library)
    * urllib (for downloading the FIDE files)
    * xml (for XML parsing)
    * tabulate (for pretty printing the output on the terminal)
    * argparse (for handling command-line arguments)

You will also need to install sqlite3 (https://www.sqlitetutorial.net/download-install-sqlite/)


## Installation
Download the files fide_download.py and fide_query.py from this repository and all the requiered python modules 

```
pip install tabulate
```

