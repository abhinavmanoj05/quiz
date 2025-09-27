import os
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

open_api_key = os.getenv("API_KEY")
llm = OpenAI(
    api_key=open_api_key,
    base_url='https://openrouter.ai/api/v1'
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        extract = request.form['extract']
        topic = request.form['topic']
        difficulty = request.form['difficulty']
        # Generate MCQ quiz questions using LLM
        prompt = (
            f"Generate 10 multiple choice questions (MCQ) for a quiz on the topic '{topic}' at '{difficulty}' difficulty level. "
            f"Base the questions on the following text. Ensure all questions are relevant to the topic and difficulty. "
            f"For each question, provide 4 options and indicate the correct option. "
            f"Format: Question|Option1|Option2|Option3|Option4|CorrectOption (number 1-4). "
            f"Text: {extract}"
        )
        messages = [{"role": "user", "content": prompt}]
        response = llm.chat.completions.create(
            model="x-ai/grok-4-fast:free",
            messages=messages
        )
        # Parse response
        lines = [line for line in response.choices[0].message.content.split('\n') if line.strip()]
        questions = []
        for line in lines:
            parts = line.split('|')
            if len(parts) == 6:
                questions.append({
                    'question': parts[0],
                    'options': parts[1:5],
                    'correct': int(parts[5])
                })
        session['questions'] = questions
        session['extract'] = extract
        session['topic'] = topic
        session['difficulty'] = difficulty
        return redirect(url_for('quiz'))
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = session.get('questions', [])
    total = len(questions)
    current = session.get('current_q', 0)
    answers = session.get('answers', [None]*total)
    if request.method == 'POST':
        # Save answer for current question
        ans = request.form.get('answer')
        answers[current] = ans
        session['answers'] = answers
        # Navigation
        if 'next' in request.form:
            current = min(current + 1, total - 1)
        elif 'prev' in request.form:
            current = max(current - 1, 0)
        elif 'submit' in request.form:
            session['current_q'] = 0
            return redirect(url_for('result'))
        session['current_q'] = current
    return render_template('quiz.html', question=questions[current], qnum=current, total=total, answer=answers[current], is_last=(current==total-1), is_first=(current==0))

@app.route('/result')
def result():
    extract = session.get('extract', '')
    questions = session.get('questions', [])
    answers = session.get('answers', [])
    # Score MCQ answers and give suggestions using LLM
    score = 0
    feedback = []
    for i, q in enumerate(questions):
        correct = str(q['correct'])
        user_ans = answers[i]
        if user_ans == correct:
            score += 1
        feedback.append(f"Q{i+1}: {'Correct' if user_ans == correct else 'Incorrect'} (Your answer: Option {user_ans}, Correct: Option {correct})")
    # Suggestions from LLM
    prompt = (
        f"Text: {extract}\nQuestions: {[q['question'] for q in questions]}\nAnswers: {answers}\n"
        f"Score: {score}/{len(questions)}. Give suggestions to improve quiz performance."
    )
    messages = [{"role": "user", "content": prompt}]
    response = llm.chat.completions.create(
        model="x-ai/grok-4-fast:free",
        messages=messages
    )
    suggestions = response.choices[0].message.content
    result = f"Score: {score}/{len(questions)}\n" + '\n'.join(feedback) + f"\n\nSuggestions:\n{suggestions}"
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5050)
