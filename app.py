# app.py
from flask import Flask, render_template, request, jsonify
import json
import os
import random

app = Flask(__name__)

# Ρύθμιση διαδρομής για το φάκελο lessons
LESSONS_FOLDER = os.path.join(os.path.dirname(__file__), 'lessons')

def load_questions(subject, difficulty):
    file_path = os.path.join(LESSONS_FOLDER, subject, f"{difficulty}.json")
    print("Αναζητούμε το αρχείο:", file_path)  # Προσθέτει έλεγχο διαδρομής
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Δεν βρέθηκε το αρχείο:", file_path)
        return None


@app.route('/')
def index():
    """Αρχική σελίδα για επιλογή μαθήματος και βαθμού δυσκολίας."""
    subjects = [f for f in os.listdir(LESSONS_FOLDER) if os.path.isdir(os.path.join(LESSONS_FOLDER, f))]
    return render_template('index.html', subjects=subjects)

@app.route('/get_question', methods=['GET'])
def get_question():
    """Επιστρέφει μία τυχαία ερώτηση για το επιλεγμένο μάθημα και βαθμό δυσκολίας."""
    subject = request.args.get('subject')
    difficulty = request.args.get('difficulty')
    questions = load_questions(subject, difficulty)
    if questions:
        question = random.choice(questions)
        return jsonify(question)
    return jsonify({"error": "Το μάθημα ή η βαθμίδα δυσκολίας δεν βρέθηκε"}), 404

if __name__ == '__main__':
    app.run(debug=True)
