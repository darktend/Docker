# app.py
from flask import Flask, request, redirect, url_for, render_template_string
import psycopg2
from psycopg2 import OperationalError
import time
import logging
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    conn = create_connection()
    if not conn:
        return "Error: Unable to connect to the database", 500

    if request.method == "POST":
        content = request.form["content"]
        with conn.cursor() as cur:
            cur.execute("INSERT INTO entries (content) VALUES (%s)", (content,))
            conn.commit()
        conn.close()
        return redirect(url_for('index'))

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM entries")
        entries = cur.fetchall()

    conn.close()

    html = """
    <!doctype html>
    <title>Flask PostgreSQL App</title>
    <h1>Enter data</h1>
    <form method=post>
      <input type=text name=content>
      <input type=submit value=Submit>
    </form>
    <h2>Entries</h2>
    <ul>
      {% for entry in entries %}
        <li>{{ entry[1] }}</li>
      {% endfor %}
    </ul>
    """
    return render_template_string(html, entries=entries)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)