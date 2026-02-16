from flask import Flask, render_template, request
import sqlite3
from datetime import datetime
from utils.calculator import calculate_total

app = Flask(__name__)

# Define database file
DATABASE = "database.db"


# -----------------------------
# Database Initialization
# -----------------------------
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            travel REAL,
            electricity REAL,
            diet REAL,
            total REAL,
            yearly REAL,
            score INTEGER,
            category TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


# Run DB initialization at startup
init_db()


# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    data = request.form

    # Calculate from calculator.py
    result_data = calculate_total(data)

    # Save to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history 
        (travel, electricity, diet, total, yearly, score, category, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        result_data["travel"],
        result_data["electricity"],
        result_data["diet"],
        result_data["total"],
        result_data["yearly"],
        result_data["score"],
        result_data["category"],
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    conn.commit()
    conn.close()

    return render_template("result.html", result=result_data)


@app.route("/history")
def history():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    records = cursor.fetchall()

    conn.close()

    return render_template("history.html", data=records)


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
