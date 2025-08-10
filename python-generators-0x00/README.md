# Streaming SQL Rows with Python Generators

## Objective

Create a Python generator that streams rows from an SQL database one by one.

---

## Table of Contents

- [Objective](#objective)
- [Database Setup](#database-setup)
- [Sample Data](#sample-data)
- [Functions Overview](#functions-overview)
- [Usage](#usage)

---

## Database Setup

First, set up a SQL database with the following table:

```sql
CREATE TABLE user_data (
    user_id UUID DEFAULT gen_random_uuid() PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL NOT NULL
);
```

---

## Sample Data

Populate the database with sample data. For example:

```sql
INSERT INTO user_data (name, email, age)
VALUES ('Johnnie Mayer', 'Ross.Reynolds21@hotmail.com', 35);
```

You can also use a CSV file (`user_data.csv`) to insert multiple records.

---

## Functions Overview

Implement the following functions in your Python code:

- **`connect_db()`**  
  Connects to the database server.

- **`create_db(connection)`**  
  Creates the database `ALX_prodev` if it does not exist.

- **`connect_to_prodev(connection)`**  
  Connects to the `ALX_prodev` database.

- **`create_table(connection)`**  
  Creates the `user_data` table if it does not exist, with the required fields.

- **`insert_data(connection, data)`**  
  Inserts data into the database if it doesn't already exist.

---

## Usage

1. **Set up the database and table** using the provided SQL statements.
2. **Populate the table** with sample data or from `user_data.csv`.
3. **Implement the Python functions** as described above.
4. **Create a generator** to stream rows from the `user_data` table one by one.

---

## Example

```python
def stream_user_data(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
```

---

## License

This project is for educational purposes.