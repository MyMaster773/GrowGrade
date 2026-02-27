from flask import Flask, render_template, request, jsonify, session, g, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' #

DATABASE = os.path.join(os.path.dirname(__file__), "quiz.db")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/video-classes')
def video_classes():
    return render_template('vc.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gs.html')
def get_started():
    return render_template('gs.html')

@app.route('/quiz')
def quiz_page():
    # Security: Redirect if no selection exists or if page was reloaded
    if 'user_selection' not in session:
        return redirect('/gs.html')
    return render_template('quiz.html')

@app.route('/api/select-path', methods=['POST'])
def select_path():
    data = request.get_json()
    session['user_selection'] = {
        'grade': str(data.get('grade')),
        'subject': str(data.get('subject')).lower(),
        'module': str(data.get('module'))
    }
    return jsonify({"status": "success", "redirect": "/quiz"}), 200

@app.route('/api/get-quiz', methods=['GET'])
def get_quiz():
    selection = session.get('user_selection')
    if not selection:
        return jsonify({"error": "Session expired"}), 400

    db = get_db()
    quiz_questions = []
    for difficulty in ["easy", "medium", "hard"]:
        rows = db.execute("""
            SELECT * FROM questions
            WHERE grade = ? AND subject = ? 
              AND module = ? AND difficulty = ?
            ORDER BY RANDOM() LIMIT 5
        """, (selection["grade"], selection["subject"], selection["module"], difficulty)).fetchall()
        quiz_questions.extend([dict(row) for row in rows])

    if not quiz_questions:
        return jsonify({"error": "No questions found"}), 404

    # Reload protection: Clear selection from session
    session.pop('user_selection', None)
    return jsonify(quiz_questions)

@app.route('/api/save-score', methods=['POST'])
def save_score():
    data = request.get_json()
    performance = data.get('performance')
    total = data.get('total')

    print("\n" + "="*30)
    print("QUIZ COMPLETED")
    print(f"Performance: {performance}")
    print(f"Total Questions: {total}")
    print("="*30 + "\n")
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)