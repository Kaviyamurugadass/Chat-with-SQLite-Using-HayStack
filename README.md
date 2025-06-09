SQL Lite Database Query Interface for Absenteeism Data
This project provides a simple web interface to query an absenteeism database using SQL. It uses Gradio for the UI and SQLite for the backend database.
🌟 Features

🔍 Query the absenteeism database with custom SQL SELECT statements
📊 View results in a formatted table with interactive interface
🛡️ Security-focused: Only SELECT queries allowed
📋 Database schema viewer
📝 Pre-built sample queries for common analyses
🎨 Modern, user-friendly web interface
⚡ Fast local SQLite database

🚀 Quick Start
Prerequisites

Python 3.7 or higher
Absenteeism_at_work.csv file in the project directory

Installation

Clone or download the project files
Install dependencies:
bashpip install gradio pandas
(The sqlite3 module comes with Python by default)
Or install from requirements file:
bashpip install -r requirements.txt

Prepare the database:

Ensure Absenteeism_at_work.csv is present in the project directory
Run the database creation script:
bashpython sql_lite.py



Start the application:
bashpython app.py

Access the interface:

Open the provided local URL in your browser (typically http://127.0.0.1:7860)
Enter SQL SELECT queries and explore your data!



📁 Project Structure
absenteeism-query-interface/
├── app.py                    # Main Gradio application
├── sql_lite.py              # Database creation script
├── requirements.txt         # Python dependencies
├── README.md               # This documentation
├── Absenteeism_at_work.csv # Source data (you need to provide this)
└── absenteeism.db          # Generated SQLite database
🔧 File Descriptions

app.py: Main application with Gradio interface and query execution logic
sql_lite.py: Script to create the SQLite database from the CSV file
requirements.txt: List of required Python packages
Absenteeism_at_work.csv: Source data file (must be provided by user)
absenteeism.db: Generated SQLite database file

💡 Usage Examples
Basic Queries
sql-- View first 5 records
SELECT * FROM absenteeism LIMIT 5;

-- Get total number of records
SELECT COUNT(*) as total_records FROM absenteeism;

-- View specific columns
SELECT ID, Absenteeism_time_in_hours, Reason_for_absence FROM absenteeism LIMIT 10;
Sample Analysis Questions
📊 General Absenteeism Analysis

What is the average absenteeism time?
sqlSELECT AVG(Absenteeism_time_in_hours) as avg_absenteeism_hours FROM absenteeism;

Which employee has the highest absenteeism time?
sqlSELECT ID, Absenteeism_time_in_hours 
FROM absenteeism 
ORDER BY Absenteeism_time_in_hours DESC 
LIMIT 1;

How many employees have disciplinary failures?
sqlSELECT COUNT(*) as employees_with_disciplinary_failures 
FROM absenteeism 
WHERE Disciplinary_failure = 1;


📈 Pattern Analysis

Total absenteeism time grouped by reason for absence:
sqlSELECT Reason_for_absence, 
       COUNT(*) as cases,
       SUM(Absenteeism_time_in_hours) as total_hours,
       AVG(Absenteeism_time_in_hours) as avg_hours
FROM absenteeism 
GROUP BY Reason_for_absence 
ORDER BY total_hours DESC;

Which month has the most absenteeism cases?
sqlSELECT Month_of_absence, 
       COUNT(*) as cases,
       SUM(Absenteeism_time_in_hours) as total_hours
FROM absenteeism 
WHERE Month_of_absence > 0
GROUP BY Month_of_absence 
ORDER BY cases DESC;

Absenteeism patterns by day of the week:
sqlSELECT Day_of_the_week,
       COUNT(*) as cases,
       AVG(Absenteeism_time_in_hours) as avg_hours
FROM absenteeism
GROUP BY Day_of_the_week
ORDER BY Day_of_the_week;


🛡️ Security Features

Query Validation: Only SELECT statements are allowed
SQL Injection Protection: Uses parameterized queries where applicable
Error Handling: Comprehensive error messages for debugging
Local Database: Data stays on your local machine

🎨 Interface Features

Modern UI: Clean, intuitive Gradio interface
Sample Queries: Pre-built queries for common analyses
Schema Viewer: Explore database structure
Interactive Results: Sortable and searchable result tables
Real-time Feedback: Immediate query results and error messages

🔍 Advanced Usage
Complex Analysis Queries
sql-- Employees with above-average transportation expenses
SELECT * FROM absenteeism 
WHERE Transportation_expense > (
    SELECT AVG(Transportation_expense) FROM absenteeism
);

-- Top 5 reasons for absence by frequency
SELECT Reason_for_absence, 
       COUNT(*) as frequency,
       ROUND(AVG(Absenteeism_time_in_hours), 2) as avg_hours
FROM absenteeism 
GROUP BY Reason_for_absence 
ORDER BY frequency DESC 
LIMIT 5;

-- Monthly absenteeism trends
SELECT Month_of_absence,
       COUNT(*) as total_cases,
       SUM(Absenteeism_time_in_hours) as total_hours,
       ROUND(AVG(Absenteeism_time_in_hours), 2) as avg_hours_per_case
FROM absenteeism
WHERE Month_of_absence BETWEEN 1 AND 12
GROUP BY Month_of_absence
ORDER BY Month_of_absence;
📊 Data Understanding
The absenteeism dataset typically contains columns such as:

Employee ID
Absenteeism time in hours
Reason for absence
Month and day of absence
Transportation expenses
Disciplinary failure indicators
And more...

Use the "Show Schema" button in the interface to see the complete structure.
🚨 Troubleshooting
Common Issues

"Database file not found" error:

Make sure you've run python sql_lite.py first
Ensure Absenteeism_at_work.csv is in the correct directory


"CSV file not found" error:

Download the absenteeism dataset and place it in the project directory
Ensure the filename is exactly Absenteeism_at_work.csv


Package import errors:

Install required packages: pip install gradio pandas
Check your Python version (3.7+ required)


Query syntax errors:

Remember only SELECT queries are allowed
Use proper SQL syntax
Check column names using the schema viewer



🔮 Future Enhancements

Natural language to SQL conversion
Data visualization charts
Export results to CSV/Excel
Query history and favorites
Advanced security features
Multi-table support

📝 Notes

Safety First: Only SELECT queries are permitted to prevent data modification
Performance: SQLite provides fast queries for datasets up to several GB
Portability: Entire database is contained in a single file
Development: Add input sanitization for production use

🤝 Contributing
Feel free to submit issues, fork the repository, and create pull requests for any improvements.
📄 License
This project is open source. Feel free to use and modify as needed.

📸 Interface Preview
The interface includes:

SQL query input area
Sample query buttons
Execute/Clear/Schema buttons
Results table display
Information panel
Sample questions guide

Start exploring your absenteeism data today! 🚀

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