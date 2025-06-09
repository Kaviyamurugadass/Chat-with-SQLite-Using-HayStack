from urllib.request import urlretrieve
from zipfile import ZipFile
import pandas as pd

# Download absenteeism dataset
url = "https://archive.ics.uci.edu/static/public/445/absenteeism+at+work.zip"
urlretrieve(url, "Absenteeism_at_work_AAA.zip")

# Extract the CSV file
with ZipFile("Absenteeism_at_work_AAA.zip", 'r') as zf:
    zf.extractall()

# Read and clean the data
csv_file_name = "Absenteeism_at_work.csv"
df = pd.read_csv(csv_file_name, sep=";")
df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.replace('/', '_')
df.head()
