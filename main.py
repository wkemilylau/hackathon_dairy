from flask import Flask, render_template, request
from datetime import datetime, timedelta

#########
import os

app = Flask(__name__)



def get_all_dates_in_month(year, month):
    """Generate all dates for the given month."""
    num_days = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month != 12 else 31
    return [datetime(year, month, day).strftime("%Y-%m-%d") for day in range(1, num_days + 1)]

###############
def load_score():
    score = 0
    if os.path.exists('score.txt'):
        with open('score.txt', 'r') as file:
            score = int(file.read().strip())
    return score

###############
def load_stops():
    stops = []
    if os.path.exists('stops.txt'):
        with open('stops.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(', ')
                    stop_name = parts[0].split(': ')[1]
                    score_required = int(parts[1].split(': ')[1])
                    stops.append({'name': stop_name, 'score_required': score_required})
    return stops


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    # Set default month and year to the current month and year
    current_date = datetime.now()
    selected_year = current_date.year
    selected_month = current_date.month

    if request.method == 'POST':
        selected_year = int(request.form.get('year'))
        selected_month = int(request.form.get('month'))

    all_dates = get_all_dates_in_month(selected_year, selected_month)

    # Get the starting weekday of the first date in the selected month
    first_date = datetime(selected_year, selected_month, 1)
    start_weekday = first_date.weekday()  # Monday = 0, Sunday = 6

    records = {}
    # Read and parse the content from the text file
    with open('answers_sample.txt', 'r') as file:
        for line in file:
            if 'date:' in line and 'prompt:' in line and 'answer:' in line:
                parts = line.strip().split('date: ')[1].split(' prompt: ')
                date = parts[0]
                rest = parts[1].split(' answer: ')
                prompt = rest[0]
                answer = rest[1]
                records[date] = {'prompt': prompt, 'answer': answer}

    return render_template('calendar.html', all_dates=all_dates, records=records, selected_year=selected_year,
                           selected_month=selected_month, start_weekday=start_weekday)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/chapters')
def chapters():
    stops = load_stops()
    user_score = load_score()
    unlocked_stops = [stop for stop in stops if user_score >= stop['score_required']
                      ]
    return render_template('chapters.html', stops=stops, user_score=user_score, unlocked_stops=unlocked_stops)


@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')


if __name__ == '__main__':
    app.run(debug=True)

