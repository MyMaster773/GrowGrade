import sqlite3
import re

def parse_file(filepath, difficulty):
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


conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()

# Insert for maths module 5
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