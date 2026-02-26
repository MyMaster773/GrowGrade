import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), "quiz.db")
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# These must match your JS exactly for the quiz to show up!
grade = "8"
subject = "maths"
module = "Algebra Basics"
difficulty = "easy"

# Format: (grade, subject, module, difficulty, question, option_a, option_b, option_c, option_d, correct_answer)
questions_to_add = [
    (grade, subject, module, difficulty, "The square of 7 is:", "14", "21", "49", "77", "C"),
    (grade, subject, module, difficulty, "Which of the following is a perfect square?", "20", "25", "30", "35", "B"),
    (grade, subject, module, difficulty, "Square root of 64 is:", "6", "7", "8", "9", "C"),
    (grade, subject, module, difficulty, "1² equals:", "0", "1", "2", "-1", "B"),
    (grade, subject, module, difficulty, "Square of an even number is:", "Odd", "Even", "Prime", "Negative", "B"),
    (grade, subject, module, difficulty, "Square of a negative number is:", "Negative", "Positive", "Zero", "Odd", "B"),
    (grade, subject, module, difficulty, "Which is not a perfect square?", "16", "36", "48", "81", "C"),
    (grade, subject, module, difficulty, "The square root of 1 is:", "0", "1", "-1", "Both B and C", "D"),
    (grade, subject, module, difficulty, "Square of 10 is:", "20", "50", "100", "1000", "C"),
    (grade, subject, module, difficulty, "Square roots are always:", "Negative", "Positive", "Zero", "Non-negative", "D")
]

query = '''
    INSERT INTO questions (grade, subject, module, difficulty, question, option_a, option_b, option_c, option_d, correct_answer)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''

try:
    cursor.executemany(query, questions_to_add)
    conn.commit()
    print("Successfully added 10 correctly formatted questions!")
except Exception as e:
    print(f"Error: {e}")

conn.close()