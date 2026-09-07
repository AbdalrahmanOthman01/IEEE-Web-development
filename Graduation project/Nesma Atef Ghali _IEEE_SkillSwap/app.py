from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import uuid

app = Flask(__name__)
app.secret_key = "skillswap-secret-key"
app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== Database ====================
def get_db():
    conn = sqlite3.connect("skillswap.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        bio TEXT DEFAULT '',
        teach TEXT DEFAULT '',
        learn TEXT DEFAULT '',
        avatar TEXT DEFAULT '',
        college TEXT DEFAULT '',
        governorate TEXT DEFAULT '',
        category TEXT DEFAULT 'Development',
        available INTEGER DEFAULT 1,
        gender TEXT DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS swap_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(sender_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(receiver_id) REFERENCES users(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(sender_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(receiver_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    # Add new columns when using an older SkillSwap database.
    columns = {row[1] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
    for name in ["college", "governorate", "category", "available", "gender"]:
        if name not in columns:
            conn.execute(f"ALTER TABLE users ADD COLUMN {name} TEXT DEFAULT ''")
    conn.commit()
    conn.close()


# All Egyptian governorates used by the Matches filter.
ALL_GOVERNORATES = [
    "Cairo", "Alexandria", "Giza", "Qalyubia", "Port Said", "Suez",
    "Luxor", "Aswan", "Asyut", "Beheira", "Beni Suef", "Dakahlia",
    "Damietta", "Faiyum", "Gharbia", "Ismailia", "Kafr El Sheikh",
    "Matrouh", "Minya", "Monufia", "New Valley", "North Sinai",
    "Qena", "Red Sea", "Sharqia", "Sohag", "South Sinai"
]

# ==================== Demo People ====================
DEMO_PEOPLE = [
    {"id": -1, "name": "Mariam Hassan", "role": "Frontend Developer", "teach": "HTML, CSS & JavaScript", "learn": "Python", "category": "Development", "gender": "Female", "college": "Menoufia University", "governorate": "Menoufia", "avatar": "/static/images/profiles/mariam.png", "available": 1},
    {"id": -2, "name": "Omar Adel", "role": "Graphic Designer", "teach": "Figma & Photoshop", "learn": "Web Development", "category": "Design", "gender": "Male", "college": "Ain Shams University", "governorate": "Cairo", "avatar": "/static/images/profiles/omar.png", "available": 1},
    {"id": -3, "name": "Salma Youssef", "role": "English Speaker", "teach": "English Conversation", "learn": "Python Basics", "category": "Languages", "gender": "Female", "college": "Menoufia University", "governorate": "Menoufia", "avatar": "/static/images/profiles/salma.png", "available": 0},
    {"id": -4, "name": "Youssef Ali", "role": "Python Developer", "teach": "Python & Flask", "learn": "HTML & CSS", "category": "Development", "gender": "Male", "college": "Tanta University", "governorate": "Gharbia", "avatar": "/static/images/profiles/youssef.png", "available": 1},
    {"id": -5, "name": "Lina Mohamed", "role": "UI/UX Designer", "teach": "Figma & UX Research", "learn": "JavaScript", "category": "Design", "gender": "Female", "college": "Helwan University", "governorate": "Cairo", "avatar": "/static/images/profiles/lina.png", "available": 1},
    {"id": -6, "name": "Adam Samir", "role": "Content Creator", "teach": "Video Editing & Writing", "learn": "Web Design", "category": "Business", "gender": "Male", "college": "Mansoura University", "governorate": "Dakahlia", "avatar": "/static/images/profiles/adam.png", "available": 0},
]


def current_user():
    if "user_id" not in session:
        return None
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()
    conn.close()
    return user


@app.context_processor
def global_data():
    return {"current_user": current_user()}


# ==================== Home ====================
@app.route("/")
def home():
    return render_template("index.html")


# ==================== Authentication ====================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm_password = request.form.get("confirm_password", "")
        if not name or not email or not password or not confirm_password:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("signup"))
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("signup"))
        conn = get_db()
        try:
            conn.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)", (name, email, generate_password_hash(password)))
            conn.commit()
            conn.close()
            flash("Account created successfully. Now complete your profile.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            conn.close()
            flash("This email is already registered.", "error")
            return redirect(url_for("signup"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("profile"))
        flash("Incorrect email or password.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


# ==================== Explore ====================
@app.route("/explore")
def explore():
    if not current_user():
        return redirect(url_for("login"))
    search = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "All")
    conn = get_db()
    real_people = conn.execute("SELECT * FROM users WHERE id != ? ORDER BY name", (session["user_id"],)).fetchall()
    request_rows = conn.execute("SELECT sender_id, receiver_id, status FROM swap_requests WHERE sender_id=? OR receiver_id=?", (session["user_id"], session["user_id"])).fetchall()
    conn.close()

    people = DEMO_PEOPLE + [dict(row) for row in real_people]
    filtered = []
    for person in people:
        text = " ".join(str(person.get(key, "")) for key in ["name", "role", "teach", "learn", "college", "governorate", "category"]).lower()
        if search and search not in text:
            continue
        if category != "All" and person.get("category") != category:
            continue
        filtered.append(person)

    request_map = {}
    for row in request_rows:
        other = row["receiver_id"] if row["sender_id"] == session["user_id"] else row["sender_id"]
        request_map[other] = row["status"] if row["sender_id"] == session["user_id"] else "received"
    return render_template("explore.html", people=filtered, search=search, category=category, request_map=request_map)


@app.route("/request/<int:user_id>", methods=["POST"])
def send_request(user_id):
    if not current_user():
        return redirect(url_for("login"))
    if user_id < 0 or user_id == session["user_id"]:
        flash("Demo profiles are for exploring the idea. Create a real account to exchange with real users.", "error")
        return redirect(url_for("explore"))
    conn = get_db()
    target = conn.execute("SELECT available FROM users WHERE id=?", (user_id,)).fetchone()
    if not target or not target["available"]:
        conn.close()
        flash("This person is currently not available for a new swap.", "error")
        return redirect(url_for("explore"))
    exists = conn.execute("SELECT id FROM swap_requests WHERE sender_id=? AND receiver_id=? AND status='pending'", (session["user_id"], user_id)).fetchone()
    if not exists:
        conn.execute("INSERT INTO swap_requests(sender_id,receiver_id) VALUES(?,?)", (session["user_id"], user_id))
        conn.commit()
        flash("Swap request sent!", "success")
    else:
        flash("You already sent a request to this person.", "error")
    conn.close()
    return redirect(url_for("explore"))


# ==================== Requests ====================
@app.route("/requests")
def requests_page():
    if not current_user():
        return redirect(url_for("login"))
    conn = get_db()
    received = conn.execute("""
        SELECT r.*, u.name, u.bio, u.teach, u.learn, u.avatar, u.college, u.governorate, u.gender
        FROM swap_requests r JOIN users u ON u.id=r.sender_id
        WHERE r.receiver_id=? ORDER BY r.id DESC
    """, (session["user_id"],)).fetchall()
    sent = conn.execute("""
        SELECT r.*, u.name, u.bio, u.teach, u.learn, u.avatar, u.college, u.governorate, u.gender
        FROM swap_requests r JOIN users u ON u.id=r.receiver_id
        WHERE r.sender_id=? ORDER BY r.id DESC
    """, (session["user_id"],)).fetchall()
    conn.close()
    return render_template("requests.html", received=received, sent=sent)


@app.route("/request/<int:request_id>/<action>", methods=["POST"])
def handle_request(request_id, action):
    if not current_user() or action not in ("accept", "reject"):
        return redirect(url_for("requests_page"))
    conn = get_db()
    row = conn.execute("SELECT * FROM swap_requests WHERE id=? AND receiver_id=? AND status='pending'", (request_id, session["user_id"])).fetchone()
    if not row:
        conn.close()
        return redirect(url_for("requests_page"))
    status = "accepted" if action == "accept" else "rejected"
    conn.execute("UPDATE swap_requests SET status=? WHERE id=?", (status, request_id))
    if action == "accept":
        conn.execute("INSERT INTO messages(sender_id,receiver_id,message) VALUES(?,?,?)", (session["user_id"], row["sender_id"], "🎉 You are now SkillSwap partners! You can start chatting."))
        flash("Request accepted. You can now chat!", "success")
    else:
        flash("Request rejected.", "error")
    conn.commit()
    conn.close()
    return redirect(url_for("requests_page"))


# ==================== Matches ====================
def skill_words(value):
    """Turn a skill text into simple searchable keywords."""
    cleaned = (value or "").lower()
    for char in [",", "/", "&", "-", "·", "|", ";"]:
        cleaned = cleaned.replace(char, " ")
    return {word.strip() for word in cleaned.split() if len(word.strip()) > 2}


def has_skill_match(my_teach, my_learn, other_teach, other_learn):
    """A match needs a two-way exchange: I can teach what they want, and vice versa."""
    my_teach_words = skill_words(my_teach)
    my_learn_words = skill_words(my_learn)
    other_teach_words = skill_words(other_teach)
    other_learn_words = skill_words(other_learn)

    first_way = bool(my_teach_words & other_learn_words)
    second_way = bool(my_learn_words & other_teach_words)
    return first_way and second_way


def get_skill_matches():
    me = current_user()
    conn = get_db()
    real_people = conn.execute("SELECT * FROM users WHERE id != ? ORDER BY name", (session["user_id"],)).fetchall()
    accepted_ids = {
        row["receiver_id"] if row["sender_id"] == session["user_id"] else row["sender_id"]
        for row in conn.execute("SELECT sender_id, receiver_id FROM swap_requests WHERE (sender_id=? OR receiver_id=?) AND status='accepted'", (session["user_id"], session["user_id"])).fetchall()
    }
    pending_rows = conn.execute("SELECT sender_id, receiver_id, status FROM swap_requests WHERE sender_id=? OR receiver_id=?", (session["user_id"], session["user_id"])).fetchall()
    conn.close()

    people = DEMO_PEOPLE + [dict(row) for row in real_people]
    matches = []
    for person in people:
        if not has_skill_match(me["teach"], me["learn"], person.get("teach", ""), person.get("learn", "")):
            continue

        person["accepted"] = person.get("id") in accepted_ids
        person["demo"] = person.get("id", 0) < 0
        person["request_status"] = ""
        for row in pending_rows:
            other_id = row["receiver_id"] if row["sender_id"] == session["user_id"] else row["sender_id"]
            if other_id == person.get("id"):
                person["request_status"] = row["status"] if row["sender_id"] == session["user_id"] else "received"
                break
        matches.append(person)
    return matches


@app.route("/matches")
def matches():
    if not current_user():
        return redirect(url_for("login"))

    governorate = request.args.get("governorate", "All").strip()
    gender = request.args.get("gender", "All").strip()
    people = get_skill_matches()

    if governorate != "All":
        people = [person for person in people if person.get("governorate") == governorate]
    if gender != "All":
        people = [person for person in people if person.get("gender") == gender]

    return render_template("matches.html", people=people, governorates=ALL_GOVERNORATES, all_governorates=ALL_GOVERNORATES, selected_governorate=governorate, selected_gender=gender)


# ==================== Chat ====================
def are_partners(other_id):
    conn = get_db()
    row = conn.execute("""
        SELECT id FROM swap_requests WHERE status='accepted'
        AND ((sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)) LIMIT 1
    """, (session["user_id"], other_id, other_id, session["user_id"])).fetchone()
    conn.close()
    return row is not None


@app.route("/chat")
@app.route("/chat/<int:other_id>")
def chat(other_id=None):
    if not current_user():
        return redirect(url_for("login"))
    conn = get_db()
    partners = conn.execute("""
        SELECT DISTINCT u.* FROM users u JOIN swap_requests r
        ON ((r.sender_id=? AND r.receiver_id=u.id) OR (r.receiver_id=? AND r.sender_id=u.id))
        WHERE u.id != ? AND r.status='accepted' ORDER BY u.name
    """, (session["user_id"], session["user_id"], session["user_id"])).fetchall()
    selected = None
    messages = []
    if other_id and are_partners(other_id):
        selected = conn.execute("SELECT * FROM users WHERE id=?", (other_id,)).fetchone()
        messages = conn.execute("""
            SELECT * FROM messages WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?) ORDER BY id
        """, (session["user_id"], other_id, other_id, session["user_id"])).fetchall()
    conn.close()
    return render_template("chat.html", partners=partners, selected=selected, messages=messages)


@app.route("/chat/<int:other_id>/send", methods=["POST"])
def send_message(other_id):
    if not current_user() or not are_partners(other_id):
        return redirect(url_for("matches"))
    message = request.form["message"].strip()
    if message:
        conn = get_db()
        conn.execute("INSERT INTO messages(sender_id,receiver_id,message) VALUES(?,?,?)", (session["user_id"], other_id, message))
        conn.commit()
        conn.close()
    return redirect(url_for("chat", other_id=other_id))


# ==================== Profile ====================
@app.route("/profile")
def profile():
    if not current_user():
        return redirect(url_for("login"))
    user = current_user()
    completed = bool(user["bio"] or user["teach"] or user["learn"] or user["avatar"] or user["college"] or user["governorate"])
    return render_template("profile.html", profile_user=user, completed=completed)


@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    if not current_user():
        return redirect(url_for("login"))
    if request.method == "POST":
        bio = request.form.get("bio", "").strip()
        teach = request.form.get("teach", "").strip()
        learn = request.form.get("learn", "").strip()
        college = request.form.get("college", "").strip()
        governorate = request.form.get("governorate", "").strip()
        category = request.form.get("category", "Development")
        gender = request.form.get("gender", "")
        available = 1 if request.form.get("available") == "1" else 0
        avatar = current_user()["avatar"] or ""

        image = request.files.get("avatar")
        if image and image.filename:
            if not allowed_file(image.filename):
                flash("Please upload a JPG, PNG, WEBP, or GIF image.", "error")
                return redirect(url_for("edit_profile"))
            extension = image.filename.rsplit(".", 1)[1].lower()
            safe_name = f"user_{session['user_id']}_{uuid.uuid4().hex[:10]}.{extension}"
            image.save(os.path.join(UPLOAD_FOLDER, secure_filename(safe_name)))
            avatar = f"/static/uploads/{safe_name}"

        conn = get_db()
        conn.execute("""UPDATE users SET bio=?, teach=?, learn=?, avatar=?, college=?, governorate=?, category=?, gender=?, available=? WHERE id=?""", (bio, teach, learn, avatar, college, governorate, category, gender, available, session["user_id"]))
        conn.commit()
        conn.close()
        flash("Profile saved successfully!", "success")
        return redirect(url_for("profile"))
    return render_template("edit_profile.html", profile_user=current_user())


@app.errorhandler(413)
def file_too_large(error):
    flash("Image is too large. Please choose an image smaller than 3 MB.", "error")
    return redirect(url_for("edit_profile"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)