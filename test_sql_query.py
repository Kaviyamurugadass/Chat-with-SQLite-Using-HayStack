from sql_component import SQLQuery

# Initialize the SQLQuery with your database file
sql_query = SQLQuery(r'C:\Users\Kaviya\Kaviya works\New folder\absenteeism.db')

# Example query to test the component
query = '''
SELECT Age, SUM("Absenteeism time in hours") as Total_Absenteeism_Hours
FROM absenteeism
WHERE "Disciplinary failure" = 0
GROUP BY Age
ORDER BY Total_Absenteeism_Hours DESC
LIMIT 3;
'''

result = sql_query.run(queries=[query])
print(result["results"][0])
