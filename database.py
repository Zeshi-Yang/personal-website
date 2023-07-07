import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# # Define the SQL statement to create a new table
# create_table_query = '''
# CREATE TABLE programming_projects (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title TEXT NOT NULL,
#     content TEXT NOT NULL,
#     full_title TEXT NOT NULL
# )
# '''

# # Execute the CREATE TABLE statement
# cursor.execute(create_table_query)



# cursor.execute('PRAGMA table_info(research_projects)')

# cursor.execute("ALTER TABLE introductions ADD COLUMN full_title text")  
# cursor.execute("ALTER TABLE introductions RENAME TO research_projects;")  
# cursor.execute("UPDATE research_projects SET id=? WHERE id = ?", ('3', '20'))
# cursor.execute("UPDATE introductions SET id=? WHERE id = ?", ('2', '3'))
# cursor.execute("UPDATE introductions SET title = ?, full_title=? WHERE id = ?", ('Powder Spreading', 'Powder segregation in powder spreading', '3'))
# cursor.execute("UPDATE research_projects SET content=? WHERE id = ?", ('This is an introduction of powder spreading. \n This paragraph should be displayed in a new line.', '3'))

# # Define the data for the new row
new_row_data = ('Website development', 
                'A learning-log website to document thoughts and notes on various topics of interest.\nWebsite Link: https://zeshiyang.pythonanywhere.com', 
                'Website development')

# # Execute the INSERT statement
cursor.execute("INSERT INTO programming_projects (title, content, full_title) VALUES (?, ?, ?)", new_row_data)


# Execute the DELETE statement
# cursor.execute("DELETE FROM research_projects WHERE id = ?", ('5'))

# cursor.execute("SELECT * FROM research_projects")
cursor.execute("SELECT * FROM programming_projects")

data = cursor.fetchall()  # Fetch all the rows returned by the query
for row in data:
    print(row)

# conn.commit()

conn.close()