import sqlite3
conn=sqlite3.connect("attendance.db")

cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
student_id TEXT UNIQUE NOT NULL,
name TEXT NOT NULL,
embedding BLOB NOT NULL)
""")

def add_student(id,student_id,name,embedding):
    conn=sqlite3.connect("attendance.db")
    cursor=conn.cursor()
    embedding_blob=embedding.astype("float32").tobytes()
    # (512,) Numpy array is converted to bytes and stored in the database as BLOB
    cursor.execute(
        "INSERT INTO students (id,student_id,name,embedding) VALUES (?,?,?,?)",
        (id,student_id,name,embedding_blob)
    )
    # insert student id + name + embedding into the db
conn.commit()
conn.close()

import numpy as np
test_embedding=np.random.rand(512).astype("float32")
add_student(1,"5001","Sahir",test_embedding)
print("Student added")