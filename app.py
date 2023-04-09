from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


RESPONSES_LIST = "responses"
survey_length = len(survey.questions)

@app.route("/")
def get_survey():
    """Show survey title, instructions, and a button to start survey."""
    title = survey.title
    instructions = survey.instructions
    
    return render_template("home.html", title=title, instructions=instructions)
    
@app.route("/begin", methods=['POST'])
def start_survey():
    session[RESPONSES_LIST] = []
    return redirect('/questions/0')



@app.route("/questions/<int:qid>")
def show_question(qid):
    """Show question/choices. Redirect if the URL is invalid."""
    question_num = qid
    responses = session.get(RESPONSES_LIST)

    if (responses is None):
        return redirect("/")

    if question_num > len(responses):
        flash("That is an invalid request. Here is the next question:", "error")
        return redirect(f"/questions/{len('responses')}")

    question = survey.questions[qid].question
    choices = survey.questions[qid].choices
    
    if question_num >= (survey_length):
        return redirect(f"/questions/{len(responses)}")
    else:
        return render_template('question.html', question=question, question_num=qid, choices=choices)
        
@app.route("/answer", methods=["POST"])
def show_answers():
    answer = request.form['choice']
    responses = session[RESPONSES_LIST]
    responses.append(answer)
    session[RESPONSES_LIST] = responses
    if len(responses) == len(survey.questions):
        return redirect("/thanks")
    return redirect(f"/questions/{len(responses)}")

@app.route("/thanks")
def give_thanks():
    
    questions = survey.questions
    return render_template("thanks.html", questions=questions)