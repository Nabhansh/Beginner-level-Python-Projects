# ============================================================
# PROJECT 5: Quiz App
# ============================================================

import random
import time

QUESTIONS = [
    {
        "question": "What is the output of print(2 ** 3)?",
        "options": ["6", "8", "9", "16"],
        "answer": "B",
        "explanation": "2 ** 3 means 2 to the power of 3 = 8"
    },
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["func", "function", "def", "define"],
        "answer": "C",
        "explanation": "'def' is used to define functions in Python"
    },
    {
        "question": "What data type is the result of: type(3.14)?",
        "options": ["int", "float", "double", "decimal"],
        "answer": "B",
        "explanation": "3.14 is a floating point number, so its type is 'float'"
    },
    {
        "question": "Which of these is NOT a Python data structure?",
        "options": ["list", "tuple", "array", "dictionary"],
        "answer": "C",
        "explanation": "Python doesn't have a built-in 'array' type (though the array module exists). list, tuple, dict are built-in."
    },
    {
        "question": "What does len([1, 2, 3, 4, 5]) return?",
        "options": ["4", "5", "6", "3"],
        "answer": "B",
        "explanation": "The list has 5 elements, so len() returns 5"
    },
    {
        "question": "What symbol is used for single-line comments in Python?",
        "options": ["//", "/*", "#", "--"],
        "answer": "C",
        "explanation": "Python uses # for single-line comments"
    },
    {
        "question": "Which method adds an element to the end of a list?",
        "options": ["add()", "insert()", "append()", "push()"],
        "answer": "C",
        "explanation": "list.append() adds an element to the end of the list"
    },
    {
        "question": "What is the correct way to create a dictionary in Python?",
        "options": ["d = []", "d = ()", "d = {}", "d = <>" ],
        "answer": "C",
        "explanation": "Dictionaries are created with curly braces {}"
    },
    {
        "question": "What does the 'break' statement do in a loop?",
        "options": ["Pauses the loop", "Skips current iteration", "Exits the loop", "Restarts the loop"],
        "answer": "C",
        "explanation": "'break' immediately exits the loop"
    },
    {
        "question": "Which Python function converts a string to an integer?",
        "options": ["str()", "float()", "int()", "num()"],
        "answer": "C",
        "explanation": "int() converts a string (or float) to an integer"
    },
    {
        "question": "What is the index of the first element in a Python list?",
        "options": ["1", "0", "-1", "None"],
        "answer": "B",
        "explanation": "Python uses 0-based indexing, so the first element is at index 0"
    },
    {
        "question": "What does the 'pass' keyword do in Python?",
        "options": ["Exits the function", "Returns None", "Does nothing (placeholder)", "Skips to next line"],
        "answer": "C",
        "explanation": "'pass' is a null operation used as a placeholder"
    },
]

def display_question(num, total, q_data):
    print(f"\n{'='*50}")
    print(f"Question {num}/{total}")
    print(f"{'='*50}")
    print(f"\n{q_data['question']}\n")
    for i, opt in enumerate(q_data['options']):
        letter = chr(65 + i)
        print(f"  {letter}) {opt}")
    print()

def run_quiz():
    print("=" * 50)
    print("         🧠 PYTHON QUIZ APP")
    print("=" * 50)
    print("Test your Python knowledge!\n")

    name = input("Enter your name: ").strip() or "Player"

    print("\nDifficulty (number of questions):")
    print("  1. Easy   (5 questions)")
    print("  2. Medium (8 questions)")
    print("  3. Hard   (12 questions)")
    choice = input("Choose (1/2/3): ").strip()

    num_questions = {"1": 5, "2": 8, "3": 12}.get(choice, 5)

    questions = random.sample(QUESTIONS, min(num_questions, len(QUESTIONS)))
    score = 0
    results = []
    start_time = time.time()

    for i, q in enumerate(questions, 1):
        display_question(i, len(questions), q)

        while True:
            answer = input("Your answer (A/B/C/D): ").strip().upper()
            if answer in ['A', 'B', 'C', 'D']:
                break
            print("Please enter A, B, C, or D")

        correct = answer == q['answer']
        if correct:
            score += 1
            print("  ✅ CORRECT!")
        else:
            correct_option = q['options'][ord(q['answer']) - 65]
            print(f"  ❌ Wrong! Correct answer: {q['answer']}) {correct_option}")

        print(f"  💡 {q['explanation']}")
        results.append({"question": q['question'], "your_answer": answer,
                         "correct_answer": q['answer'], "is_correct": correct})

    elapsed = time.time() - start_time
    percentage = (score / len(questions)) * 100

    print("\n" + "=" * 50)
    print(f"         📊 RESULTS FOR {name.upper()}")
    print("=" * 50)
    print(f"  Score: {score}/{len(questions)}  ({percentage:.1f}%)")
    print(f"  Time:  {elapsed:.1f} seconds")

    if percentage == 100: grade, msg = "A+", "🏆 Perfect score! Outstanding!"
    elif percentage >= 80: grade, msg = "A",  "🌟 Excellent work!"
    elif percentage >= 60: grade, msg = "B",  "👍 Good job! Keep practicing!"
    elif percentage >= 40: grade, msg = "C",  "📚 Keep studying!"
    else:                  grade, msg = "D",  "💪 Don't give up, practice more!"

    print(f"  Grade: {grade}  {msg}")
    print("=" * 50)

if __name__ == "__main__":
    run_quiz()
    while input("\nPlay again? (y/n): ").lower() == 'y':
        run_quiz()
    print("\nThanks for playing! 🎓")
