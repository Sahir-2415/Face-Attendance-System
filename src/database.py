import sqlite3
conn=sqlite3.connect("attendance.db")
from datetime import datetime
cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
student_id TEXT UNIQUE NOT NULL,
name TEXT NOT NULL,
embedding BLOB NOT NULL)
""")

def add_student(student_id,name,embedding):
    conn=sqlite3.connect("attendance.db")
    cursor=conn.cursor()
    embedding_blob=embedding.astype("float32").tobytes()
    # (512,) Numpy array is converted to bytes and stored in the database as BLOB
    cursor.execute(
        "INSERT INTO students (student_id,name,embedding) VALUES (?,?,?)",
        (student_id,name,embedding_blob)
    )
    # insert student id + name + embedding into the db
    conn.commit()
    conn.close()

def get_students():
    conn=sqlite3.connect("attendance.db")
    cursor=conn.cursor()
    cursor.execute("SELECT student_id,name,embedding FROM students")
    students=cursor.fetchall()
    conn.close()
    return students

def create_attendance_table():
    conn=sqlite3.connect("attendance.db")
    cursor=conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    UNIQUE(student_id,date))""")
    conn.commit()
    conn.close()

def mark_attendance(student_id):
    conn=sqlite3.connect("attendance.db")
    cursor=conn.cursor()
    now=datetime.now()
    date=now.strftime("%Y-%m-%d")
    time=now.strftime("%H:%M:%S")
    try:
        cursor.execute(
            "INSERT INTO attendance(student_id,date,time) VALUES (?,?,?)",
            (student_id,date,time)
        )
        conn.commit()
        print("Attendance marked")
    except sqlite3.IntegrityError:
        print("Attendance already marked for today")
    conn.close()

import numpy as np
# test_embedding=np.random.rand(512).astype("float32")
# add_student("5001","Sahir",test_embedding)
# print("Student added")

students=get_students()
print(students)
for student in students:
    student_id,name,embedding_blob=student
    embedding=np.frombuffer(embedding_blob,dtype="float32")
    print(student_id)
    print(name)
    print(embedding.shape)

# COMMENTED LINES ARE JUST FOR TESTING PURPOSES AND CAN BE UNCOMMENTED TO TEST THE DATABASE FUNCTIONALITY.

create_attendance_table()
# mark_attendance("5001")