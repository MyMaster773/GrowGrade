import os
import sqlite3
import re

def parse_file(filepath, difficulty):
    # make filepath absolute relative to this script if necessary
    if not os.path.isabs(filepath):
        base = os.path.dirname(__file__)
        filepath = os.path.join(base, filepath)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Question file not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.strip().split("Ans:")

    questions = []

    for block in blocks[:-1]:
        parts = block.strip().split("\n")
        question = parts[0].strip()
        options = [p.strip() for p in parts[1:5]]

        ans_letter = blocks[blocks.index(block)+1].strip()[0]

        questions.append({
            "question": question,
            "a": options[0][3:].strip(),
            "b": options[1][3:].strip(),
            "c": options[2][3:].strip(),
            "d": options[3][3:].strip(),
            "answer": ans_letter
        })

    return questions


# open the database living next to this script so we're always in the
# same location that you inspect with the sqlite3 shell
base = os.path.dirname(__file__)
db_path = os.path.join(base, "quiz.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# optionally, ensure the table exists before inserting
cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        grade TEXT, subject TEXT, module TEXT, difficulty TEXT,
        question TEXT, option_a TEXT, option_b TEXT,
        option_c TEXT, option_d TEXT, correct_answer TEXT
    )
""")

# Insert for maths module 5
# files are expected to live alongside this script (GrowGrade folder)
for difficulty, file in [
    ("hard", "hard.txt"),
    ("medium", "med.txt"),
    ("easy", "easy.txt")  # when you add it
]:
    questions = parse_file(file, difficulty)

    for q in questions:
        cursor.execute("""
            INSERT INTO questions 
            (grade, subject, module, difficulty, question, 
             option_a, option_b, option_c, option_d, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "8",
            "maths",
            "5",
            difficulty,
            q["question"],
            q["a"],
            q["b"],
            q["c"],
            q["d"],
            q["answer"]
        ))

conn.commit()
conn.close()