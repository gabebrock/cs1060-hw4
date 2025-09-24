import sys
import csv
import sqlite3
import os

# parse the Command-Line Arguments
# if database and data file are not provided, exit with error
if len(sys.argv) != 3:
    sys.exit("Missing arguments. Usage: python csv_to_sqlite.py <database_name.db> <csv_file_name.csv>")
else:
    if sys.argv[1].endswith(".db") == False:
        sys.exit("Database name must end with .db")
    elif sys.argv[2].endswith(".csv") == False:
        sys.exit("CSV file name must end with .csv")

# store arguments
db = sys.argv[1]
csv_file = sys.argv[2]

# get table name from csv file name
table = os.path.splitext(os.path.basename(csv_file))[0]
table = table.replace(" ", "_").replace("-", "_").lower()
print(f"Table name: {table}")

# connect to SQLite database
connection = sqlite3.connect(db)
cursor = connection.cursor()

# check if table exists // claude
def check_table_exists(table):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
    return cursor.fetchone() is not None

# Parse the CSV File
'''
Open the CSV file with the built-in csv module.
Read the header row for column names.
Column names must:
    match the header row in the file.
    contain no spaces or special characters, so they should directly map to SQL column names as per the assignment.
'''

# based on Stack Answer from Jan 21, 2014 at 14:55
# https://stackoverflow.com/questions/21257899/writing-a-csv-file-into-sql-server-database-using-python

with open(csv_file, 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    header = next(reader)

    # clean headers for SQL table
    columns = []
    for col in header:
        col = col.replace(" ", "_").replace("-", "_").lower()
        columns.append(col)
    print(f"Columns: {columns}")

    # create table first
    if not check_table_exists(table):
        columns_def = ', '.join([f"{col} TEXT" for col in columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table} ({columns_def})"
        cursor.execute(create_table_query)

    # write data to SQL table
    with open(csv_file, 'r', encoding='utf-8-sig') as file:  # Handle BOM character
        reader = csv.reader(file)
        header = next(reader)
        print(f"Clean headers: {columns}")

        # insert data from CSV to SQL table
        placeholders = ', '.join(['?' for _ in header]) # claude
        data_insert_query = f"INSERT INTO {table} VALUES ({placeholders})"
        row_count = 0
    
        for data in reader:
            cursor.execute(data_insert_query, data)
            row_count += 1
        connection.commit()
        print(f"Successfully inserted {row_count} rows into table '{table}'")
    



