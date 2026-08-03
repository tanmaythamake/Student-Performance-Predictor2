from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- PREDICT ----------------

@app.route("/predict", methods=["GET", "POST"])
def predict():

    result = None

    if request.method == "POST":

        name = request.form["name"]
        attendance = float(request.form["attendance"])
        study = float(request.form["study"])
        internal = float(request.form["internal"])
        assignment = float(request.form["assignment"])
        previous = float(request.form["previous"])

        score = (
            attendance * 0.20 +
            study * 5 +
            internal * 0.30 +
            assignment * 0.20 +
            previous * 0.30
        )

        if score > 100:
            score = 100

        if score >= 90:
            grade = "A+"
        elif score >= 80:
            grade = "A"
        elif score >= 70:
            grade = "B+"
        elif score >= 60:
            grade = "B"
        elif score >= 50:
            grade = "C"
        elif score >= 40:
            grade = "D"
        else:
            grade = "F"

        if score >= 75:
            risk = "Low"
        elif score >= 50:
            risk = "Medium"
        else:
            risk = "High"

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO students
        (name, attendance, study_hours,
        internal_marks,
        assignment_marks,
        previous_marks,
        predicted_score,
        grade,
        risk)

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            attendance,
            study,
            internal,
            assignment,
            previous,
            round(score,2),
            grade,
            risk
        ))

        conn.commit()
        conn.close()

        result = {
            "name": name,
            "score": round(score,2),
            "grade": grade,
            "risk": risk
        }

    return render_template("predict.html", result=result)
# ---------------- HISTORY ----------------

@app.route("/history")
def history():

    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id DESC")

    students = cursor.fetchall()

    conn.close()

    return render_template("history.html", students=students)


# ---------------- ABOUT ----------------

@app.route("/about")
def about():
    return render_template("about.html")


# ---------------- SETTINGS ----------------

@app.route("/settings")
def settings():
    return render_template("settings.html")


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)