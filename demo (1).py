from flask import Flask, render_template, request, jsonify
import csv
from nltk.chat.util import Chat
import webbrowser

app = Flask(__name__)

def load_responses_from_csv(file_path):
    responses = []

    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) == 2:
                question, answer = row
                responses.append([rf"{question}", [f"chatbot: {answer}"]])
            else:
                print(f"Skipping invalid row: {row}")

    return responses

if __name__ == "__main__":
    responses = load_responses_from_csv('dialogs.csv')
    if not responses:
        print("No valid responses found. Please check your dataset.")
    else:
        chat = Chat(responses)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/get_response', methods=['POST'])
    def get_response():
        user_input = request.form['user_input']

        if user_input.lower() == 'open youtube':
            response = "opening youtube"
            webbrowser.open('https://www.youtube.com')
        elif user_input.lower() == 'open google':
            response = "opening google"
            webbrowser.open('https://www.google.com')
        else:
            response = chat.respond(user_input)

        return jsonify({'response': response})

    app.run(debug=True)
