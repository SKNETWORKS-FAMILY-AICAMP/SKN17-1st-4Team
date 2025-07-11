import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='skn_1st_4team',
    password='skn_1st_4team',
    database='densedb'
)
cursor = conn.cursor()

faq_df = pd.read_csv('company_faq_data.csv')

insert_query = """
INSERT INTO company_faq (question_id, company_name, question, answer)
VALUES (%s, %s, %s, %s)
"""

for _, row in faq_df.iterrows():
    cursor.execute(insert_query, (row['question_id'], row['company_name'], row['question'], row['answer']))

conn.commit()
cursor.close()
conn.close()