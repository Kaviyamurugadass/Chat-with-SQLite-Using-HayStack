# Read.md

## SQL Database Query Interface for Absenteeism Data

This project provides a simple web interface to query an absenteeism database using SQL. It uses [Gradio](https://gradio.app/) for the UI and SQLite for the backend database.

### Features

- Query the absenteeism database with custom SQL `SELECT` statements.
- View results in a formatted table.
- Easy-to-use web interface.

### Setup

1. **Install dependencies:**
    ```sh
    pip install gradio pandas
    ```
    (The `sqlite3` module comes with Python.)

2. **Prepare the database:**
    - Ensure `Absenteeism_at_work.csv` is present in the project directory.
    - Run the following script to create the SQLite database:
        ```sh
        python sql_lite.py
        ```

3. **Start the application:**
    ```sh
    python app.py
    ```

4. **Access the interface:**
    - Open the provided local URL in your browser.
    - Enter a SQL `SELECT` query (e.g., `SELECT * FROM absenteeism LIMIT 5;`).

### Files

- [`app.py`](app.py): Main application with Gradio interface.
- [`sql_lite.py`](sql_lite.py): Script to create the SQLite database from the CSV file.
- `Absenteeism_at_work.csv`: Source data.
- `absenteeism.db`: Generated SQLite database.

### Notes

- Only `SELECT` queries are allowed for safety.
- For production use, add input sanitization and/or natural language to SQL conversion.

---

UI of this project
![Screenshot 2025-06-09 112427](https://github.com/user-attachments/assets/8f993129-d5c6-4549-b799-8b5353b78b54)

--- 

### Sample questions
 📊 General Absenteeism Questions
 - What is the average absenteeism time?

 - Which employee has the highest absenteeism time?

 - How many employees have disciplinary failures?

 - What is the total absenteeism time grouped by reason for absence?

 - Which month has the most absenteeism cases?

 - List the top 5 departments with the most absenteeism.