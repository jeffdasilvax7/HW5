import mysql.connector as mysql
from datetime import date

cfg = dict(host="127.0.0.1", port=3306, user="root", password="Jeffrey123", database="db_registra")
conn = mysql.connect(**cfg)
cur = conn.cursor()

cur.execute("SELECT DATABASE(), @@hostname, @@port;")
print("Connected to:", cur.fetchone())

cur.execute("""
INSERT INTO tbl_student (first_name, last_name, email, birthdate)
VALUES (%s, %s, %s, %s)
ON DUPLICATE KEY UPDATE first_name=VALUES(first_name)
""", ("Test", "User", "test@example.com", date(2010,1,1)))
conn.commit()

cur.execute("SELECT st_ID, first_name, last_name, email, birthdate FROM tbl_student WHERE email=%s", ("test@example.com",))
print("Row:", cur.fetchone())

cur.close()
conn.close()
