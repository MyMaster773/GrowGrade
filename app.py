from flask import Flask, render_template, request, jsonify, session, g

import sqlite3
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # Needed to use sessions

DATABASE = os.path.join(os.path.dirname(__file__), "quiz.db")
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gs.html')
def get_started():
    # It still looks inside the 'templates' folder for the actual file
    return render_template('gs.html')

@app.route('/api/select-path', methods=['POST'])
def select_path():
    data = request.get_json()
    
    # Extract the data
    grade = data.get('grade')
    subject = data.get('subject')
    module = data.get('module')

    # Store in session so you can use it on the next page
    session['user_selection'] = {
        'grade': str(grade),
        'subject': str(subject).lower(),
        'module': str(module)
    }

    print(f"Flask received: Grade {grade}, Subject {subject}, Module {module}")

    # for now redirect back to home; later this can point to /lesson or another page
    return jsonify({"status": "success", "redirect": "/api/get-quiz"}), 200

@app.route('/api/get-quiz', methods=['GET'])
def get_quiz():
    selection = session.get('user_selection')

    if not selection:
        return jsonify({"error": "No selection found in session"}), 400

    db = get_db()

    quiz_questions = []

    for difficulty in ["easy", "medium", "hard"]:
        rows = db.execute("""
            SELECT * FROM questions
            WHERE grade = ? AND subject = ? 
              AND module = ? AND difficulty = ?
            ORDER BY RANDOM()
            LIMIT 5
        """, (
            selection["grade"],
            selection["subject"],
            selection["module"],
            difficulty
        )).fetchall()

        quiz_questions.extend([dict(row) for row in rows])

    if not quiz_questions:
        return jsonify({"error": "No questions found"}), 404

    session["current_quiz"] = quiz_questions

    return jsonify(quiz_questions)
if __name__ == '__main__':
    app.run(debug=True)