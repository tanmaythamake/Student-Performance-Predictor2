from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
import joblib
import os

app = Flask(__name__)

# =========================================================
# POSTGRESQL DATABASE CONFIGURATION
# =========================================================

# Render/Neon DATABASE_URL असेल तर तो वापरेल.
# Local computer वर DATABASE_URL नसेल तर खालील PG variables वापरेल.

DATABASE_URL = os.environ.get("DATABASE_URL")


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():

    # -----------------------------------------------------
    # Render + Neon connection
    # -----------------------------------------------------

    if DATABASE_URL:

        conn = psycopg2.connect(
            DATABASE_URL,
            sslmode="require"
        )

        return conn

    # -----------------------------------------------------
    # Fallback for local computer
    # -----------------------------------------------------

    PG_HOST = os.environ.get(
        "PG_HOST",
        "localhost"
    )

    PG_PORT = os.environ.get(
        "PG_PORT",
        "5432"
    )

    PG_DATABASE = os.environ.get(
        "PG_DATABASE",
        "postgres"
    )

    PG_USER = os.environ.get(
        "PG_USER",
        "postgres"
    )

    PG_PASSWORD = os.environ.get(
        "PG_PASSWORD",
        ""
    )

    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD
    )

    return conn


# =========================================================
# LOAD MACHINE LEARNING MODEL
# =========================================================

model = joblib.load("model.pkl")


# =========================================================
# HOME / DASHBOARD
# =========================================================

@app.route("/")
def home():

    conn = get_db_connection()

    cursor = conn.cursor(
        cursor_factory=RealDictCursor
    )

    # -----------------------------------------------------
    # Latest Student
    # -----------------------------------------------------

    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY id DESC
        LIMIT 1
    """)

    student = cursor.fetchone()

    # -----------------------------------------------------
    # Total Predictions
    # -----------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM students
    """)

    total_predictions = cursor.fetchone()["total"]

    # -----------------------------------------------------
    # Average Predicted Score
    # -----------------------------------------------------

    cursor.execute("""
        SELECT AVG(predicted_score) AS average
        FROM students
    """)

    average_score = cursor.fetchone()["average"]

    if average_score is None:
        average_score = 0

    # -----------------------------------------------------
    # Average Attendance
    # -----------------------------------------------------

    cursor.execute("""
        SELECT AVG(attendance) AS average
        FROM students
    """)

    average_attendance = cursor.fetchone()["average"]

    if average_attendance is None:
        average_attendance = 0

    # -----------------------------------------------------
    # Risk Distribution
    # -----------------------------------------------------

    cursor.execute("""
        SELECT risk, COUNT(*) AS count
        FROM students
        GROUP BY risk
    """)

    risk_rows = cursor.fetchall()

    risk_data = {
        "Low": 0,
        "Medium": 0,
        "High": 0
    }

    for row in risk_rows:

        if row["risk"] in risk_data:
            risk_data[row["risk"]] = row["count"]

    # -----------------------------------------------------
    # Recent Predictions
    # -----------------------------------------------------

    cursor.execute("""
        SELECT
            id,
            name,
            predicted_score,
            grade,
            risk
        FROM students
        ORDER BY id DESC
        LIMIT 7
    """)

    recent_rows = cursor.fetchall()

    # Oldest → Newest
    recent_rows = list(
        reversed(recent_rows)
    )

    # -----------------------------------------------------
    # Graph Data
    # -----------------------------------------------------

    prediction_labels = []
    prediction_scores = []

    for index, row in enumerate(
        recent_rows,
        start=1
    ):

        prediction_labels.append(
            "Prediction " + str(index)
        )

        prediction_scores.append(
            round(
                float(row["predicted_score"]),
                2
            )
        )

    cursor.close()
    conn.close()

    return render_template(
        "index.html",

        student=student,

        total_predictions=total_predictions,

        average_score=round(
            float(average_score),
            2
        ),

        average_attendance=round(
            float(average_attendance),
            2
        ),

        risk_data=risk_data,

        prediction_labels=prediction_labels,

        prediction_scores=prediction_scores
    )


# =========================================================
# PREDICT
# =========================================================

@app.route(
    "/predict",
    methods=["GET", "POST"]
)
def predict():

    result = None

    if request.method == "POST":

        # -------------------------------------------------
        # STUDENT INFORMATION
        # -------------------------------------------------

        name = request.form["name"]

        attendance = float(
            request.form["attendance"]
        )

        study = float(
            request.form["study"]
        )

        # -------------------------------------------------
        # INTERNAL MARKS
        # -------------------------------------------------

        internal_total = float(
            request.form["internal_total"]
        )

        internal_obtained = float(
            request.form["internal_obtained"]
        )

        # -------------------------------------------------
        # ASSIGNMENT MARKS
        # -------------------------------------------------

        assignment_total = float(
            request.form["assignment_total"]
        )

        assignment_obtained = float(
            request.form["assignment_obtained"]
        )

        # -------------------------------------------------
        # PREVIOUS SEMESTER MARKS
        # -------------------------------------------------

        total_marks = float(
            request.form["total_marks"]
        )

        obtained_marks = float(
            request.form["obtained_marks"]
        )

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if internal_total <= 0:

            return (
                "Internal total marks must be "
                "greater than 0"
            )

        if assignment_total <= 0:

            return (
                "Assignment total marks must be "
                "greater than 0"
            )

        if total_marks <= 0:

            return (
                "Previous semester total marks "
                "must be greater than 0"
            )

        # -------------------------------------------------
        # CONVERT MARKS INTO PERCENTAGE
        # -------------------------------------------------

        internal = (
            internal_obtained /
            internal_total
        ) * 100

        assignment = (
            assignment_obtained /
            assignment_total
        ) * 100

        previous = (
            obtained_marks /
            total_marks
        ) * 100

        # -------------------------------------------------
        # LIMIT PERCENTAGES
        # -------------------------------------------------

        internal = max(
            0,
            min(internal, 100)
        )

        assignment = max(
            0,
            min(assignment, 100)
        )

        previous = max(
            0,
            min(previous, 100)
        )

        # =================================================
        # MACHINE LEARNING PREDICTION
        # =================================================

        data = [[
            attendance,
            study,
            internal,
            assignment,
            previous
        ]]

        score = model.predict(data)[0]

        # Keep score between 0 and 100

        if score > 100:
            score = 100

        if score < 0:
            score = 0

        score = round(
            float(score),
            2
        )

        # =================================================
        # GRADE
        # =================================================

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

        # =================================================
        # RISK
        # =================================================

        if score >= 75:

            risk = "Low"

        elif score >= 50:

            risk = "Medium"

        else:

            risk = "High"

        # =================================================
        # SAVE RESULT TO POSTGRESQL
        # =================================================

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students
            (
                name,
                attendance,
                study_hours,
                internal_marks,
                assignment_marks,
                previous_marks,
                predicted_score,
                grade,
                risk
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
                %s
            )
        """,
        (
            name,
            attendance,
            study,
            internal,
            assignment,
            previous,
            score,
            grade,
            risk
        ))

        conn.commit()

        cursor.close()
        conn.close()

        # =================================================
        # RESULT
        # =================================================

        result = {

            "name": name,

            "score": score,

            "grade": grade,

            "risk": risk
        }

    return render_template(
        "predict.html",
        result=result
    )


# =========================================================
# HISTORY
# =========================================================

@app.route("/history")
def history():

    conn = get_db_connection()

    cursor = conn.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY id DESC
    """)

    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "history.html",
        students=students
    )


# =========================================================
# DELETE STUDENT RECORD
# =========================================================

@app.route(
    "/delete/<int:student_id>",
    methods=["POST"]
)
def delete_student(student_id):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM students
        WHERE id = %s
        """,
        (student_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(
        url_for("history")
    )


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# =========================================================
# SETTINGS
# =========================================================

@app.route("/settings")
def settings():

    return render_template(
        "settings.html"
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),
        debug=False
    )
