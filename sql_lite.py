import sqlite3
import pandas as pd

# Load your CSV file (update path accordingly)
df = pd.read_csv('Absenteeism_at_work.csv', sep=';')

# Connect to DB or create if not exists
conn = sqlite3.connect('absenteeism.db')

# Write dataframe to SQL table 'absenteeism'
df.to_sql('absenteeism', conn, if_exists='replace', index=False)

conn.close()