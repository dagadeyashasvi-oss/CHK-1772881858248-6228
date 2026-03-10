from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():

    conn = sqlite3.connect("food.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS food(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT,
        city TEXT,
        event_place TEXT,
        contact TEXT,
        food_type TEXT,
        quantity TEXT,
        expiry TEXT,
        latitude TEXT,
        longitude TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    event_name = request.form["event_name"]
    city = request.form["city"]
    event_place = request.form["event_place"]
    contact = request.form["contact"]
    food_type = request.form["food_type"]
    quantity = request.form["quantity"]
    expiry = request.form["expiry"]
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]

    conn = sqlite3.connect("food.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO food(event_name,city,event_place,contact,food_type,quantity,expiry,latitude,longitude)
    VALUES (?,?,?,?,?,?,?,?,?)
    """,(event_name,city,event_place,contact,food_type,quantity,expiry,latitude,longitude))

    conn.commit()
    conn.close()

    return redirect("/ngo")


@app.route("/ngo")
def ngo():

    conn = sqlite3.connect("food.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM food")
    data = cur.fetchall()

    conn.close()

    return render_template("ngoinfo.html",data=data)


if __name__ == "__main__":
    app.run(debug=True)