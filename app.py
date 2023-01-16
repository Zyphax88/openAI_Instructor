import os

import openai
from flask import Flask, render_template, request
from dotenv import load_dotenv

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
historyChat = []
tokenPrompt = 0
tokenCompletion = 0
tokenTotal = 0

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        studentInput = request.form["studentInput"]
        historyChat.append("Student: " + studentInput)
        
        # openAI API
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(studentInput),
            temperature=0.6,
            max_tokens=400,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )
        historyChat.append(response.choices[0].text)
        tokenPrompt = response.usage.prompt_tokens
        tokenCompletion = response.usage.completion_tokens
        tokenTotal = response.usage.total_tokens

        return render_template("index.html", historyChat=historyChat, tokenPrompt=tokenPrompt, tokenCompletion=tokenCompletion, tokenTotal=tokenTotal)

    return render_template("index.html", historyChat=historyChat, tokenPrompt=0, tokenCompletion=0, tokenTotal=0)

def readStudyGuide():
    # Used for testing API without wasting tokens
    with open("static/Test_Prompt.txt", "r", encoding="utf-8") as file:
        currentStudyGudie = file.read()
        return(currentStudyGudie)
   
    # Reads actual study guide ~2K tokens required
    # with open("static/Blk3_Unit1.txt", "r", encoding="utf-8") as file:
    #     currentStudyGudie = file.read()
    #     return(currentStudyGudie)

def generate_prompt(studentInput):
    return """The following is a conversation with an AI instructor for high school graduates 
    trying to become aircraft mechanics. The AI is professional and will answer the student's 
    questions correctly.  If the student asks a question that does not pertain to aircraft or 
    mechanics please remind them to stay on topic.  Only use the following information given 
    below when helping the student. \n""" + readStudyGuide() + """\nStudent: I need help understanding aircraft mechanics
    AI Instructor: I am an AI created by OpenAI. What do you need help with today?
    Student: {}
    """.format(studentInput)
