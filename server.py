from flask import Flask, render_template, url_for , request , redirect
import csv

import pandas as pd, random




df = pd.read_csv('/home/shibz98/quizonserver/surahs-file.csv', delimiter='|')
list_surah = (set((df['surah_name']).values.ravel()))
list_surah=(sorted(list_surah))
#list_surah.sort(reverse=True)
set_to_tuple = tuple(list_surah)

zipped_data=""
surah_name=""

def process_data(x):
    userAnswer = x
    asked_surah = str(userAnswer)

    surah_data = (df[(df['surah_name'] == asked_surah)])
    surah_in_list = list()
    for row in surah_data.values:
        surah_in_list.append(row[1:])

    list_to_tuple = tuple(surah_in_list)

    def alternativesAnswers(x):
        alternatives = list()
        possible_answers = list()
        print(len(x))

        for i in x:
            alternatives.append(i[1])

        if len(x) > 3:
            for i in x:

                possible = random.sample(alternatives, 4)

                while i[1] not in possible:
                    possible = random.sample(alternatives, 4)

                if i[1] in possible:
                    possible_answers.append(possible)
        else:
            length = len(i) + 1
            for i in x:

                possible = random.sample(alternatives, length)

                while i[1] not in possible:
                    possible = random.sample(alternatives, length)

                if i[1] in possible:
                    possible_answers.append(possible)

        return possible_answers

    possible_answers = (alternativesAnswers(surah_in_list))

    zipped = list(zip(surah_in_list, possible_answers))

    random.shuffle(zipped)

    Questions = []
    Options = []
    Answers = []

    for i in zipped:
        Questions.append(i[0][0])
        Options.append(i[1][:])

        looking_answer = i[0][1]
        Answers.append((i[1].index(looking_answer) + 1))



    print("------------------------------------")

    return Questions,Options,Answers

app = Flask(__name__)
print(__name__)

@app.route('/')
def my_home():
    return redirect('/list')




@app.route('/list', methods=['GET', 'POST'])
def item_list():
    global zipped_data
    global surah_name
    items = set_to_tuple
    selected_item = None
    if request.method == 'POST':
        selected_item = request.form['item']
        print(selected_item)
        surah_name=selected_item
        zipped_data = process_data(selected_item)
        print(zipped_data)
        return redirect('/quiz')

    return render_template('surah_list.html', items=items, selected_item=selected_item)





@app.route('/quiz', methods=['GET', 'POST'])
def quiz_list():
    items = zipped_data
    questions = items[0]
    options = items[1]
    answers = items[2]

    question_length=len(questions)

    if request.method == 'POST':
        # Process form submission
        score = 0
        incorrect_answers = []  # Initialize a list to store incorrect answers
        correct_selected =[]
        for i in range(len(questions)):
            selected_answer = request.form[str(i)]
            if selected_answer == str(options[i][answers[i]-1]):
                score += 1
                correct_selected.append({
                    'question_no': i + 1,
                    'question': questions[i],
                    'selected_answer': selected_answer,
                    'correct_answer': options[i][answers[i] - 1]
                })


            else:
                incorrect_answers.append({
                    'question_no': i+1,
                    'question': questions[i],
                    'selected_answer': selected_answer,
                    'correct_answer': options[i][answers[i]-1]
                })  # Add incorrect answer to list
        return render_template('results.html', score=score, length=question_length, incorrect=incorrect_answers, correct=correct_selected)

    # Display quiz questions and options
    return render_template('quiz.html', questions=questions, options=options, surah_name=surah_name)













#---------------------Previous Code-----------------------------------

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

#---------------------Previous Code Above-----------------------------------


