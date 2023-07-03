import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM research_projects")
# cursor.execute("ALTER TABLE introductions ADD COLUMN full_title text")  
# cursor.execute("ALTER TABLE introductions RENAME TO research_projects;")  
# cursor.execute("UPDATE introductions SET title = ?, full_title=? WHERE id = ?", ('Powder Spreading', 'Powder segregation in powder spreading', '3'))
cursor.execute("UPDATE research_projects SET content=? WHERE id = ?", ('This is an introduction of powder spreading. \n This paragraph should be displayed in a new line.', '3'))
data = cursor.fetchall()  # Fetch all the rows returned by the query

for row in data:
    print(row)

conn.commit()
conn.close()