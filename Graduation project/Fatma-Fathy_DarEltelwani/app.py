
from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="WJ28@krhps",
    database="telwani_db"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/courses")
def courses():
    return render_template("courses.html")


@app.route("/learn")
def learn():
    return render_template("learn.html")


@app.route("/library")
def library():
    return render_template("library.html")


@app.route("/academy")
def academy():
    return render_template("academy.html")


@app.route("/questions")
def questions():
    return render_template("que.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/registrations")
def registrations():
    return render_template("registrations.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullName = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        email = request.form.get("email")

        courses = request.form.getlist("course")
        course_text = ", ".join(courses)

        way = request.form.get("way")
        halaqa = request.form.get("halaqa")
        level = request.form.get("level")

        days = request.form.getlist("day")
        day_text = ", ".join(days)

        notes = request.form.get("notes")


        cursor = db.cursor()


        sql = """
            INSERT INTO registrations
            (
                fullName,
                age,
                gender,
                phone,
                email,
                course,
                way,
                halaqa,
                level,
                day,
                notes
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """


        values = (
            fullName,
            age,
            gender,
            phone,
            email,
            course_text,
            way,
            halaqa,
            level,
            day_text,
            notes
        )


        cursor.execute(sql, values)

        db.commit()

        cursor.close()


        return "تم إرسال بيانات التسجيل بنجاح ❤️"


    return render_template("register.html")


@app.route("/api/admin/registrations", methods=["GET"])
def get_registrations():

    cursor = db.cursor(dictionary=True)


    sql = """
        SELECT
            id,
            fullName,
            age,
            gender,
            phone,
            email,
            course,
            way,
            halaqa,
            level,
            day,
            notes,
            created_at
        FROM registrations
        ORDER BY created_at DESC
    """


    cursor.execute(sql)

    registrations = cursor.fetchall()

    cursor.close()


    return jsonify(registrations)


@app.route("/api/questions", methods=["POST"])
def add_question():

    data = request.get_json()

    question = data.get("question")


    if not question:

        return jsonify({
            "message": "برجاء كتابة السؤال أولاً"
        }), 400


    cursor = db.cursor()


    sql = """
        INSERT INTO questions (question)
        VALUES (%s)
    """


    cursor.execute(sql, (question,))

    db.commit()

    cursor.close()


    return jsonify({
        "message":
        "تم إرسال سؤالك بنجاح وسيتم الرد عليه قريباً!"
    })


@app.route("/api/questions", methods=["GET"])
def get_questions():

    cursor = db.cursor(dictionary=True)


    sql = """
        SELECT
            id,
            question,
            answer,
            created_at
        FROM questions
        ORDER BY created_at DESC
    """


    cursor.execute(sql)

    questions = cursor.fetchall()

    cursor.close()


    return jsonify(questions)


@app.route("/api/admin/pending-questions", methods=["GET"])
def pending_questions():

    cursor = db.cursor(dictionary=True)


    sql = """
        SELECT
            id,
            question,
            answer,
            created_at
        FROM questions
        WHERE answer IS NULL
        ORDER BY created_at DESC
    """


    cursor.execute(sql)

    questions = cursor.fetchall()

    cursor.close()


    return jsonify(questions)


@app.route("/api/admin/answer-question", methods=["POST"])
def answer_question():

    data = request.get_json()


    question_id = data.get("id")
    answer = data.get("answer")


    if not question_id or not answer:

        return jsonify({
            "message": "البيانات غير مكتملة"
        }), 400


    cursor = db.cursor()


    sql = """
        UPDATE questions
        SET answer = %s
        WHERE id = %s
    """


    cursor.execute(
        sql,
        (answer, question_id)
    )


    db.commit()

    cursor.close()


    return jsonify({
        "message": "تم حفظ الإجابة بنجاح!"
    })


if __name__ == "__main__":

    app.run(debug=True)

