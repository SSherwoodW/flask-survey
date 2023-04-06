from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []
survey_length = len(survey.questions)

@app.route("/")
def get_survey():
    """Show survey title, instructions, and a button to start survey."""
    title = survey.title
    instructions = survey.instructions
    
    return render_template("home.html", title=title, instructions=instructions)
    


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Show question/choices. Redirect if the URL is invalid."""
    question_num = qid

    if question_num > len(responses):
        flash("That is an invalid request. Here is the next question:", "error")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid].question
    choices = survey.questions[qid].choices
    
    if question_num >= (survey_length):
        return redirect(f"/questions/{len(responses)}")
    else:
        return render_template('question.html', question=question, question_num=qid, choices=choices)
        
@app.route("/answer", methods=["POST"])
def show_answers():
    answer = request.form['choice']
    responses.append(answer)
    if len(responses) == len(survey.questions):
        return redirect("/thanks")
    return redirect(f"/questions/{len(responses)}")

@app.route("/thanks")
def give_thanks():
    return render_template("thanks.html")