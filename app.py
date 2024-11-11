from flask import Flask, render_template, request, jsonify
import json
import os
import random

app = Flask(__name__)

# Ρύθμιση διαδρομής για το φάκελο lessons
LESSONS_FOLDER = os.path.join(os.path.dirname(__file__), 'lessons')

def load_questions(subject, difficulty):
    file_path = os.path.join(LESSONS_FOLDER, subject, f"{difficulty}.json")
    print("Αναζητούμε το αρχείο:", file_path)
    
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

@app.route('/get_questions', methods=['GET'])
def get_questions():
    """Επιστρέφει ερωτήσεις για το επιλεγμένο μάθημα και βαθμό δυσκολίας."""
    subject = request.args.get('subject')
    difficulty = request.args.get('difficulty')
    
    print(f"Λήφθηκε αίτημα για μάθημα: {subject}, δυσκολία: {difficulty}")
    
    questions_data = load_questions(subject, difficulty)
    
    if questions_data:
        # Μετατροπή των questions σε κατάλληλη μορφή
        formatted_questions = []
        for question in questions_data:
            # Εξαγωγή του αριθμού της σωστής απάντησης
            correct_answer_index = int(question['answer']) - 1
            
            # Αντιστοίχιση του αριθμού της απάντησης με το αντίστοιχο κείμενο της επιλογής
            formatted_question = {
                'question': question['question'],
                'answers': question['choices'],
                'correct': correct_answer_index
            }
            formatted_questions.append(formatted_question)
        
        return jsonify({'questions': formatted_questions})
    
    return jsonify({"error": "Το μάθημα ή η βαθμίδα δυσκολίας δεν βρέθηκε"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)  # Άλλαξα το debug σε True για development
