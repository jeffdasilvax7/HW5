from flask import Flask, render_template, request
import mysql.connector as mysql
from datetime import date
import sys

app = Flask(__name__)

DB_CFG = {
    "host": "127.0.0.1",
    "port": 3306,  # MySQL port
    "user": "root",
    "password": "Jeffrey123",
    "database": "db_registra",
}

def save_user(first_name: str, last_name: str, email: str, birthdate_str: str):
    y, m, d = map(int, birthdate_str.split("-"))
    bdate = date(y, m, d)

    conn = mysql.connect(**DB_CFG)
    cur = conn.cursor()

    # DEBUG: show where we connected
    cur.execute("SELECT DATABASE(), @@hostname, @@port;")
    current_db, host, port = cur.fetchone()
    print(f"[DB] Connected to db={current_db} host={host} port={port}", file=sys.stderr)

    sql = """
        INSERT INTO tbl_student (first_name, last_name, email, birthdate)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
          first_name = VALUES(first_name),
          last_name  = VALUES(last_name),
          birthdate  = VALUES(birthdate);
    """
    cur.execute(sql, (first_name.strip(), last_name.strip(), email.strip(), bdate))
    conn.commit()

    # DEBUG: how many rows?
    rows = cur.rowcount
    print(f"[DB] Rows affected: {rows}", file=sys.stderr)

    # DEBUG: fetch back the row we just touched (by unique email)
    cur.execute("""
        SELECT st_ID, first_name, last_name, email, birthdate, created_at
        FROM tbl_student WHERE email=%s
    """, (email.strip(),))
    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "connected_db": current_db,
        "connected_host": host,
        "connected_port": port,
        "rows_affected": rows,
        "row": row
    }

@app.route("/", methods=["GET", "POST"])
def form():
    db_debug = None
    error = None
    submitted = False
    name = last = email = birthdate = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        last = request.form.get("last", "").strip()
        email = request.form.get("email", "").strip()
        birthdate = request.form.get("birthdate", "").strip()

        missing = [k for k,v in {"name":name, "last":last, "email":email, "birthdate":birthdate}.items() if not v]
        if missing:
            error = f"Missing fields: {', '.join(missing)}"
        else:
            try:
                db_debug = save_user(name, last, email, birthdate)
                submitted = True
            except Exception as e:
                error = f"DB error: {e}"

    return render_template("form.html",
        submitted=submitted, error=error,
        name=name, last=last, email=email, birthdate=birthdate,
        db_debug=db_debug
    )

if __name__ == "__main__":
    # Flask runs on port 5000 (web)
    app.run(host="0.0.0.0", port=5000, debug=True)
