import sqlite3

conn = sqlite3.connect("database/colleges.db")
cursor = conn.cursor()

colleges = [

(
"PSIT Kanpur",
"CSE",
150000,
6.5,
"Uttar Pradesh",
"Top engineering college in Kanpur."
),

(
"GL Bajaj",
"CSE",
190000,
8.0,
"Uttar Pradesh",
"Excellent placement records."
),

(
"NIET",
"CSE",
180000,
7.2,
"Uttar Pradesh",
"Popular college under AKTU."
)

]

cursor.executemany("""
INSERT INTO colleges
(name,course,fees,placement,state,description)
VALUES(?,?,?,?,?,?)
""", colleges)

conn.commit()
conn.close()

print("Colleges Added Successfully")