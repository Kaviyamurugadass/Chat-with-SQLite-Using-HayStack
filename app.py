import sqlite3
import re
import os
from typing import Dict, List, Tuple

class NLToSQLConverter:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.table_info = self._get_table_info()
        
    def _get_table_info(self) -> Dict:
        """Get information about tables and columns in the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            table_info = {}
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table});")
                columns = cursor.fetchall()
                table_info[table] = {
                    'columns': [col[1] for col in columns],
                    'column_types': {col[1]: col[2] for col in columns}
                }
            
            conn.close()
            return table_info
        except Exception as e:
            print(f"Error getting table info: {e}")
            return {}
    
    def _wrap_column_name(self, column_name: str) -> str:
        """Wrap column names with spaces in square brackets"""
        if ' ' in column_name or any(char in column_name for char in ['-', '/', '(', ')']):
            return f'[{column_name}]'
        return column_name
    
    def convert_nl_to_sql(self, question: str) -> str:
        """Convert natural language question to SQL query"""
        question = question.lower().strip()
        
        # Get the main table (assuming it's the absenteeism table)
        main_table = None
        for table_name in self.table_info.keys():
            if 'absent' in table_name.lower():
                main_table = table_name
                break
        
        if not main_table:
            main_table = list(self.table_info.keys())[0] if self.table_info else "absenteeism"
        
        columns = self.table_info.get(main_table, {}).get('columns', [])
        
        # Pattern matching for different types of questions
        
        # Age group questions
        if 'age group' in question and ('highest' in question or 'most' in question):
            if 'hours' in question or 'hour' in question:
                # Find hours/duration column
                hours_col = self._find_column(['hours', 'duration', 'time'], columns)
                age_col = self._find_column(['age'], columns)
                
                if hours_col and age_col:
                    hours_col_wrapped = self._wrap_column_name(hours_col)
                    age_col_wrapped = self._wrap_column_name(age_col)
                    return f"""SELECT 
    CASE 
        WHEN {age_col_wrapped} < 25 THEN '18-24'
        WHEN {age_col_wrapped} < 35 THEN '25-34'
        WHEN {age_col_wrapped} < 45 THEN '35-44'
        WHEN {age_col_wrapped} < 55 THEN '45-54'
        ELSE '55+'
    END as age_group,
    SUM({hours_col_wrapped}) as total_hours,
    COUNT(*) as absence_count,
    AVG({hours_col_wrapped}) as avg_hours
FROM {main_table}
GROUP BY age_group
ORDER BY total_hours DESC;"""
        
        # Reason questions (since there's no department column, use reason)
        if 'department' in question or 'reason' in question or 'why' in question:
            reason_col = self._find_column(['reason'], columns)
            if reason_col:
                reason_col_wrapped = self._wrap_column_name(reason_col)
                if 'highest' in question or 'most' in question:
                    if 'hours' in question:
                        hours_col = self._find_column(['hours', 'duration', 'time'], columns)
                        if hours_col:
                            hours_col_wrapped = self._wrap_column_name(hours_col)
                            return f"SELECT {reason_col_wrapped}, SUM({hours_col_wrapped}) as total_hours FROM {main_table} GROUP BY {reason_col_wrapped} ORDER BY total_hours DESC;"
                    else:
                        return f"SELECT {reason_col_wrapped}, COUNT(*) as absence_count FROM {main_table} GROUP BY {reason_col_wrapped} ORDER BY absence_count DESC;"
        
        # Employee questions (use ID since no employee name column)
        if 'employee' in question or 'person' in question or 'who' in question:
            emp_col = self._find_column(['id', 'employee', 'emp', 'person', 'name'], columns)
            if 'highest' in question or 'most' in question:
                if emp_col:
                    emp_col_wrapped = self._wrap_column_name(emp_col)
                    hours_col = self._find_column(['hours', 'duration', 'time'], columns)
                    if hours_col:
                        hours_col_wrapped = self._wrap_column_name(hours_col)
                        return f"SELECT {emp_col_wrapped}, SUM({hours_col_wrapped}) as total_hours FROM {main_table} GROUP BY {emp_col_wrapped} ORDER BY total_hours DESC LIMIT 10;"
                    else:
                        return f"SELECT {emp_col_wrapped}, COUNT(*) as absence_count FROM {main_table} GROUP BY {emp_col_wrapped} ORDER BY absence_count DESC LIMIT 10;"
        
        # Reason questions
        if 'reason' in question or 'common' in question:
            reason_col = self._find_column(['reason', 'cause', 'type'], columns)
            if reason_col:
                reason_col_wrapped = self._wrap_column_name(reason_col)
                if 'common' in question or 'frequent' in question:
                    return f"SELECT {reason_col_wrapped}, COUNT(*) as frequency FROM {main_table} GROUP BY {reason_col_wrapped} ORDER BY frequency DESC;"
        
        # Time-based questions
        if 'month' in question or 'monthly' in question:
            month_col = self._find_column(['month'], columns)
            if month_col:
                month_col_wrapped = self._wrap_column_name(month_col)
                return f"SELECT {month_col_wrapped}, COUNT(*) as absences FROM {main_table} GROUP BY {month_col_wrapped} ORDER BY {month_col_wrapped};"
        
        if 'day' in question and 'week' in question:
            day_col = self._find_column(['day'], columns)
            if day_col:
                day_col_wrapped = self._wrap_column_name(day_col)
                return f"SELECT {day_col_wrapped}, COUNT(*) as absences FROM {main_table} GROUP BY {day_col_wrapped} ORDER BY absences DESC;"
        
        # Count questions
        if 'how many' in question or 'count' in question:
            if 'total' in question:
                return f"SELECT COUNT(*) as total_records FROM {main_table};"
        
        # Average questions
        if 'average' in question or 'avg' in question:
            if 'hours' in question:
                hours_col = self._find_column(['hours', 'duration', 'time'], columns)
                if hours_col:
                    return f"SELECT AVG({hours_col}) as average_hours FROM {main_table};"
        
        # If no pattern matches, suggest some queries
        return f"""I couldn't automatically convert your question to SQL. Here are the available columns in {main_table}:
{', '.join(columns)}

Try asking questions like:
- "Which age group had the highest absenteeism hours?"
- "What department has the most absences?"
- "Who are the top 10 employees with most absence hours?"
- "What are the most common reasons for absence?"
- "Show monthly absence trends"

Or you can write a direct SQL query starting with SELECT."""
    
    def _find_column(self, keywords: List[str], columns: List[str]) -> str:
        """Find a column that matches any of the keywords"""
        for keyword in keywords:
            for col in columns:
                if keyword.lower() in col.lower():
                    return col
        return None

class DatabaseChat:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.converter = NLToSQLConverter(db_path)
        
    def execute_query(self, query: str) -> str:
        """Execute SQL query and return formatted results"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Get column names
            column_names = [description[0] for description in cursor.description] if cursor.description else []
            
            if not results:
                conn.close()
                return "No results found."
            
            # Format results as a table
            formatted_output = []
            
            # Add headers
            if column_names:
                header = " | ".join(f"{col:15}" for col in column_names)
                formatted_output.append(header)
                formatted_output.append("-" * len(header))
            
            # Add data rows (limit to first 20 rows for readability)
            for i, row in enumerate(results[:20]):
                formatted_row = " | ".join(f"{str(cell) if cell is not None else 'NULL':15}" for cell in row)
                formatted_output.append(formatted_row)
            
            if len(results) > 20:
                formatted_output.append(f"\n... and {len(results) - 20} more rows")
            
            conn.close()
            return "\n".join(formatted_output)
            
        except sqlite3.Error as e:
            return f"SQL Error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat(self, user_input: str) -> Tuple[str, str]:
        """Main chat function that returns both SQL and results"""
        user_input = user_input.strip()
        
        # Check if it's already a SQL query
        if user_input.upper().startswith('SELECT'):
            sql_query = user_input
            generated = False
        else:
            sql_query = self.converter.convert_nl_to_sql(user_input)
            generated = True
        
        # Execute the query
        results = self.execute_query(sql_query)
        
        return sql_query, results, generated

def main():
    db_path = "absenteeism.db"
    
    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found!")
        print("Please ensure the database file is in the same directory as this script.")
        return
    
    chat_bot = DatabaseChat(db_path)
    
    print("=" * 70)
    print("🤖 DATABASE CHAT - Ask questions in natural language!")
    print("=" * 70)
    print("Examples:")
    print("• Which age group had the highest absenteeism hours?")
    print("• What department has the most absences?")
    print("• Who are the top employees with most absence hours?")
    print("• What are the most common reasons for absence?")
    print("• Show me monthly trends")
    print("\nOr type SQL queries directly. Type 'quit' to exit.")
    print("=" * 70)
    
    while True:
        try:
            user_question = input("\n🗣️  Ask your question: ").strip()
            
            if user_question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_question:
                continue
            
            # Get SQL and results
            sql_query, results, was_generated = chat_bot.chat(user_question)
            
            if was_generated:
                print(f"\n🔍 Generated SQL:")
                print(f"   {sql_query}")
            
            print(f"\n📊 Results:")
            print(results)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()