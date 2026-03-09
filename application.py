# Flask library import for web application
from flask import Flask, render_template, request, redirect

# SQLite database library
import sqlite3

# Flask app create
app = Flask(__name__)


# Database create function
def init_db():

    # database connect
    conn = sqlite3.connect("food.db")

    # cursor create
    cur = conn.cursor()

    # table create
    cur.execute("""
    CREATE TABLE IF NOT EXISTS food(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_place TEXT,
    location TEXT,
    city TEXT,
    food_type TEXT,
    quantity TEXT,
    spoilage_time TEXT
    )
    """)

    conn.commit()
    conn.close()

# initialize database
init_db()


# home page
@app.route("/")
def index():
    return render_template("index.html")


# form submit route
@app.route("/submit", methods=["POST"])
def submit():

    # form data
    event_place = request.form["event_place"]
    location = request.form["location"]
    city = request.form["city"]
    food = request.form["food"]
    quantity = request.form["quantity"]
    spoilage = request.form["spoilage"]

    # database connect
    conn = sqlite3.connect("food.db")
    cur = conn.cursor()

    # insert data
    cur.execute("""
    INSERT INTO food (event_place,location,city,food_type,quantity,spoilage_time)
    VALUES (?,?,?,?,?,?)
    """,(event_place,location,city,food,quantity,spoilage))

    conn.commit()
    conn.close()

    return redirect("/ngo")


# NGO dashboard
@app.route("/ngo")
def ngo():

    conn = sqlite3.connect("food.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM food")
    data = cur.fetchall()

    conn.close()

    return render_template("ngoinfo.html",data=data)


# run server
if __name__ == "__main__":
    app.run(debug=True)