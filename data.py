import pandas as pd
import sqlite3
connection = sqlite3.connect("data.db")
cursor = connection.cursor()
cursor.execute("ALTER TABLE jobs_ca ADD COLUMN source TEXT")
connection.commit()

cursor.execute("""
                UPDATE jobs_ca
                SET source = "jsearch"
                WHERE source IS NULL
               """)
connection.commit()

df = pd.read_sql("SELECT * FROM jobs_ca", connection)
print(df.columns)




