from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, static_folder="templates/static")

# إنشاء قاعدة البيانات والجدول
def create_database():
    connection = sqlite3.connect("users.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT
        )
    """)

    connection.commit()
    connection.close()


create_database()


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("users.db")

        user = connection.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()

        connection.close()

        if user:
            return render_template("home.html", username=user[1])

        return "Email or password is incorrect."

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("users.db")

        connection.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )

        connection.commit()
        connection.close()

        return "Registration completed successfully!"

    return render_template("register.html")

@app.route("/home")
def home_page():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)