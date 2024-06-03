import sqlite3


def get_picture_from_db(record_id, database_file="database.db"):
    """
    This function retrieves the picture data (BLOB) from a SQLite3 database 
    given a database file path and record ID.

    Args:
        database_file: Path to the SQLite3 database file.
        record_id: The ID of the record containing the picture.

    Returns:
        The BLOB data (binary image data) retrieved from the database, 
        or None if the record is not found or has no picture.
    """

    # Connect to the database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Prepare the SELECT statement
    sql = """SELECT picture FROM places WHERE id = ?"""

    # Execute the query with the ID
    cursor.execute(sql, (record_id,))
    print(cursor.rowcount)
    # Fetch the first row
    image_data = cursor.fetchone()[0]
    print(image_data)
    # Close the connection
    conn.close()

    return image_data


def get_all_records(database_file="database.db"):
    """
    This function retrieves all records from the 'places' table in a SQLite3 database 
    and returns them as a list of dictionaries.

    Args:
        database_file: Path to the SQLite3 database file.

    Returns:
        A list of dictionaries, where each dictionary represents a record with its 
        columns (id, address, coordinates, picture) as key-value pairs.
    """

    # Connect to the database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Prepare the SELECT statement
    sql = """SELECT * FROM places"""

    # Execute the query
    cursor.execute(sql)

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Convert rows to dictionary list
    records = []
    for row in rows:
        record_dict = mapRow(row)
        records.append(record_dict)

    return records


def get_record_by_id(record_id, database_file="database.db"):
    """
    This function retrieves a record by ID from a table in a SQLite3 database.

    Args:
        database_file: Path to the SQLite3 database file.
        record_id: The ID of the record to retrieve.

    Returns:
        A dictionary containing the retrieved record's data (column values) if found,
        or None if the record is not found.
    """

    # Connect to the database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    try:
        # Prepare the SELECT statement
        sql = f"""SELECT * FROM places WHERE id = ?"""

        # Execute the query with the ID
        cursor.execute(sql, (record_id,))

        # Fetch the first row (assuming single record by ID)
        row = cursor.fetchone()

        # Close the connection (done if successful retrieval)
        conn.close()

        if row:
            # Convert row data to dictionary (column names as keys, values as elements)
            record_dict = mapRow(row)
            return record_dict
        else:
            return None

    except sqlite3.Error as error:
        # Handle database errors
        print(f"Error retrieving record: {error}")
        return None

    finally:
        # Ensure the connection is closed regardless of success or error
        if conn:
            conn.close()


def get_all_accepted_records(database_file="database.db"):
    """
    This function retrieves all records where the 'accepted' column is True 
    from a table in a SQLite3 database.

    Args:
        database_file: Path to the SQLite3 database file.
        table_name: Name of the table containing the records.

    Returns:
        A list of dictionaries, where each dictionary represents a record with its 
        columns (including 'accepted') as key-value pairs.
    """

    # Connect to the database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    try:
        # Prepare the SELECT statement
        sql = f"""SELECT * FROM places WHERE accepted = 1"""

        # Execute the query
        cursor.execute(sql)

        # Fetch all rows
        rows = cursor.fetchall()

        # Close the connection (done if successful retrieval)
        conn.close()

        # Convert rows to dictionary list
        records = []
        for row in rows:
            record_dict = mapRow(row)
            records.append(record_dict)

        return records

    except sqlite3.Error as error:
        # Handle database errors
        print(f"Error retrieving records: {error}")
        return []

    finally:
        # Ensure the connection is closed regardless of success or error
        if conn:
            conn.close()


def insert_record(address, latitude, longitude, database_file="database.db",  image_data=None):
    """
    This function inserts a record into the 'places' table of a SQLite3 database.

    Args:
        database_file: Path to the SQLite3 database file.
        address: The address of the place.
        latitude: The latitude coordinate of the place.
        longitude: The longitude coordinate of the place.
        image_data: The BLOB data (optional) containing the image for the place.

    Returns:
        True if the record is inserted successfully, False otherwise.
    """

    # Connect to the database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    try:
        # Prepare the INSERT statement with placeholders
        sql = """INSERT INTO places (address, lat, long, picture) VALUES (?, ?, ?, ?)"""

        # Bind the values including the BLOB data
        cursor.execute(sql, (address, latitude, longitude, image_data))

        # Commit changes to the database
        conn.commit()

        # Success
        return True

    except sqlite3.Error as error:
        print("Error inserting record:", error)
        return False

    finally:
        # Close the connection regardless of success or error
        conn.close()


def accept_record(record_id, database_file="database.db"):
    """
    This function updates the 'accepted' column to True for a record with the 
    specified ID in the given table.

    Args:
        database_file: Path to the SQLite3 database file.
        record_id: The ID of the record to update.

    Returns:
        True if the update is successful, False otherwise.
    """

    # Connect to the database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    try:
        # Prepare the UPDATE statement
        sql = f"""UPDATE places SET accepted = 1 WHERE id = ?"""

        # Execute the query with the ID
        cursor.execute(sql, (record_id,))

        # Commit changes to the database
        conn.commit()

        # Success
        return True

    except sqlite3.Error as error:
        print(f"Error updating record: {error}")
        return False

    finally:
        # Close the connection regardless of success or error
        conn.close()


def mapRow(row):
    return {"id": row[0], "address": row[1], "lat": row[2], "long": row[3], "accepted": row[5]}
