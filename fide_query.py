import sqlite3
import csv
import argparse
try:
    from tabulate import tabulate  # This is used to print a well-formatted table
    tabulateDO = True
except:
    print("Warning: tabulate module not installed, output will look less pretty")
    tabulateDO = False 

# Function to read FIDE IDs from the input file
def read_fide_ids(input_file):
    with open(input_file, 'r') as file:
        fide_ids = [line.strip() for line in file.readlines()]
    return fide_ids

# Function to query the database for the selected FIDE IDs
def query_fide_records(conn, fide_ids, fields):
    # Prepare the SQL query
    sql = f"SELECT {', '.join(fields)} FROM fide_ratings WHERE fide_id IN ({', '.join(['?']*len(fide_ids))})"
    
    try:
        cur = conn.cursor()
        cur.execute(sql, fide_ids)
        records = cur.fetchall()
        return records
    except sqlite3.Error as e:
        print(f"An error occurred while querying the database: {e}")
        return []

# Function to write the output to a CSV file
def write_to_csv(output_file, records, fields):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header
        writer.writerow(fields)
        
        # Write the records
        writer.writerows(records)

# Function to print records to the console
def print_to_console(records, fields):
    print("\nFIDE Records:\n")
    if records:
        if tabulateDO:
            # Use tabulate to print a well-formatted table
            print(tabulate(records, headers=fields, tablefmt='pretty'))
        else:
            print(fields)
            for record in records:
                print(record)
    else:
        print("No records found.")

# Main function to handle command-line arguments and orchestrate the process
def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Query FIDE ratings by FIDE ID and output results as CSV.")
    parser.add_argument("input_file", help="File containing FIDE IDs (one per line)")
    parser.add_argument("output_file", help="CSV file where the output should be saved")
    parser.add_argument('--fields', nargs='+', default=["fide_id", "name", "country", "rating"], 
                        help='Fields to include in the output (default: fide_id, name, country, rating). Possible fields: fide_id, name, country, sex, title, rating, games_played, rapid_rating, rapid_games INTEGER, blitz_rating, blitz_games, birthday. Example: python3 pp.py input.txt output.txt --fields "fide_id, name, country, birthday, rating"'
)
    parser.add_argument("--database", default="fide_ratings.db", help="SQLite database file (default: fide_ratings.db)")

    args = parser.parse_args()

    # Read FIDE IDs from the input file
    fide_ids = read_fide_ids(args.input_file)

    # Create a connection to the SQLite database
    conn = sqlite3.connect(args.database)

    # Query the database for the specified FIDE IDs and selected fields
    records = query_fide_records(conn, fide_ids, args.fields)

    # Close the database connection
    conn.close()

    # Write the results to the CSV file
    write_to_csv(args.output_file, records, args.fields)

    # Print the results to the console
    print_to_console(records, args.fields)

if __name__ == "__main__":
    main()

