from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizzes.db'
db = SQLAlchemy(app)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    choices = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

db.create_all()

@app.route('/')
def home():
    quizzes = Quiz.query.all()
    return render_template('index.html', quizzes=quizzes)

@app.route('/create_quiz', methods=['POST'])
def create_quiz():
    title = request.form['title']
    new_quiz = Quiz(title=title)
    db.session.add(new_quiz)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/quiz/<int:quiz_id>')
def quiz(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return render_template('quiz.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/submit_answers/<int:quiz_id>', methods=['POST'])
def submit_answers(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    score = 0
    for question in questions:
        user_answer = request.form[str(question.id)]
        if user_answer == question.answer:
            score += 1
    return f"Your score: {score}/{len(questions)}"
