# First, install the required packages:
# pip install haystack-ai
# pip install sqlite3 (usually comes with Python)
# pip install gradio

import sqlite3
import gradio as gr
from typing import List, Dict, Any

class SimpleSQLRetriever:
    def __init__(self, db_file_path: str):
        self.db_file_path = db_file_path
    
    def run(self, question: str) -> Dict[str, List[str]]:
        """
        Simple SQL query executor.
        Note: In production, you'd want to use proper SQL generation from natural language
        or sanitize inputs to prevent SQL injection.
        """
        try:
            # Connect to the database
            conn = sqlite3.connect(self.db_file_path)
            cursor = conn.cursor()
            
            # For this example, we'll assume the question is already a SQL query
            # In a real application, you'd convert natural language to SQL
            if not question.strip().upper().startswith('SELECT'):
                return {"answers": ["Please provide a valid SELECT SQL query"]}
            
            # Execute the query
            cursor.execute(question)
            results = cursor.fetchall()
            
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            # Format results
            if results:
                formatted_results = []
                formatted_results.append(" | ".join(column_names))
                formatted_results.append("-" * (len(" | ".join(column_names))))
                
                for row in results:
                    formatted_results.append(" | ".join(str(cell) for cell in row))
                
                result_string = "\n".join(formatted_results)
            else:
                result_string = "No results found"
            
            conn.close()
            return {"answers": [result_string]}
            
        except sqlite3.Error as e:
            return {"answers": [f"Database error: {str(e)}"]}
        except Exception as e:
            return {"answers": [f"Error: {str(e)}"]}

# Initialize the retriever
retriever = SimpleSQLRetriever(db_file_path="absenteeism.db")

def query_sql_database(question):
    result = retriever.run(question=question)
    return result["answers"][0]

# Create Gradio interface
demo = gr.Interface(
    fn=query_sql_database, 
    inputs=gr.Textbox(
        label="SQL Query",
        placeholder="Enter your SQL SELECT query here...",
        lines=3
    ),
    outputs=gr.Textbox(
        label="Query Results",
        lines=10
    ),
    title="SQL Database Query Interface",
    description="Enter a SQL SELECT query to retrieve data from the absenteeism database."
)

if __name__ == "__main__":
    demo.launch()