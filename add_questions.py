import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), "quiz.db")
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

grade = "8"
subject = "maths"
module = "Algebra Basics"

# Let's add 5 Medium and 5 Hard questions
questions_to_add = [
    # --- MEDIUM QUESTIONS ---
    (grade, subject, module, "medium", "If n² = 144, n =", "12", "-12", "±12", "0", "C"),
    (grade, subject, module, "medium", "√81 + √16 =", "10", "12", "13", "15", "C"), # 9 + 4 = 13
    (grade, subject, module, "medium", "Square of 15 is:", "225", "215", "235", "245", "A"),
    (grade, subject, module, "medium", "Which of the following is not a perfect square?", "169", "196", "225", "250", "D"),
    (grade, subject, module, "medium", "Square root of 0 is:", "0", "1", "Undefined", "-1", "A"),
    
    # --- HARD QUESTIONS ---
    (grade, subject, module, "hard", "If √x = 15, then x =", "30", "225", "15", "450", "B"),
    (grade, subject, module, "hard", "Which number lies between 12² and 13²?", "150", "160", "165", "170", "C"), # 144 and 169
    (grade, subject, module, "hard", "√0.09 =", "0.3", "0.03", "3", "0.9", "A"),
    (grade, subject, module, "hard", "The square of the sum of two numbers (a+b)² is:", "a² + b²", "(a + b)²", "a² + 2ab + b²", "Both B and C", "D"),
    (grade, subject, module, "hard", "Which number has an odd number of factors?", "Prime number", "Composite number", "Perfect square", "Even number", "C")
]

query = '''
    INSERT INTO questions (grade, subject, module, difficulty, question, option_a, option_b, option_c, option_d, correct_answer)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''

try:
    cursor.executemany(query, questions_to_add)
    conn.commit()
    print("Successfully added Medium and Hard questions!")
except Exception as e:
    print(f"Error: {e}")

conn.close()