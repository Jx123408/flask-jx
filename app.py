from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import sqlite3
import qrcode
import io

app = Flask(__name__)
DB_FILE = "tickets.db"
MAX_TICKETS = 50  # 整理券の上限枚数

# データベース初期化
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                event TEXT NOT NULL,
                ticket_id TEXT UNIQUE NOT NULL
            )
        """)
        conn.commit()

# QRコード生成関数
def generate_qr(ticket_id):
    qr = qrcode.make(ticket_id)
    img_io = io.BytesIO()
    qr.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io

@app.route("/")
def index():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tickets")
        count = cursor.fetchone()[0]
    
    return render_template("index.html", remaining=MAX_TICKETS - count)

@app.route("/issue", methods=["POST"])
def issue_ticket():
    name = request.form.get("name")
    event = request.form.get("event")

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tickets")
        count = cursor.fetchone()[0]

        if count >= MAX_TICKETS:
            return jsonify({"error": "整理券は上限に達しました"}), 400

        ticket_id = f"{event}-{count+1}"
        cursor.execute("INSERT INTO tickets (name, event, ticket_id) VALUES (?, ?, ?)", (name, event, ticket_id))
        conn.commit()

    return jsonify({"ticket_id": ticket_id})

@app.route("/qr/<ticket_id>")
def get_qr(ticket_id):
    img_io = generate_qr(ticket_id)
    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
