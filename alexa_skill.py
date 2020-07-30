from flask import Flask
from flask_ask import Ask, statement, question, session
import logging
from flask_ask import context

app = Flask(__name__)
ask = Ask(app, "/testalexa")

"""Setup"""
@app.route('/')
def homepage():
    return "Welcome to Intern Buddy!"

@ask.on_session_started
def start_session():
    """
    Fired at the start of the session, this is a great place to initialise state variables and the like.
    """

    session.attributes["questions"] = None
    session.attributes["question_number"] = 0
    session.attributes['device_id'] = context.System.device.deviceId
    session.attributes['user_id'] = session.user.userId

    session.attributes["questions"] = setup_questions()
    logging.warning("Questions: " + str(session.attributes["questions"]))
    uid = context.System.user.userId
    logging.warning(str(uid))

@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like to get matched?'
    return question(welcome_message)

"""Helper Functions"""
def setup_questions():
    start_text = "Requesting your preferences. Please respond with the question number and then your answer. You may say skip, proceed, or continue to ignore a question. Would you like to begin?"
    # sample response: one. Seattle.
    location_text = "One. Which city will you be working in for the upcoming summer?"
    school_text = "Two. What university or school do you currently attend?"
    group_size_text = "Three. What's your ideal group size? You can respond with small, medium, and large."
    position_type_text = "Four. What's your intern position? You can say Software Development, Business Analyst, Program Manager, etc."
    age_text = "Five. Would you like to match with undergraduates or graduates?"
    hang_out_text = "Six. Would you be willing to hang out with your buddy after work? You can say hang out or stay home."

    return [start_text, location_text, school_text, group_size_text, position_type_text, age_text, hang_out_text]

def get_preference(pref_num):
    session.attributes["question_number"] = pref_num + 1
    if pref_num == len(session.attributes["questions"]):
        print(session.attributes)
        r = requests.post('http://089af49540a4.ngrok.io/session_info', json=session.attributes)
        print(r.json())
        return statement("Analyzing your preferences. Please wait while we search for your match!")
    else:
        current_question = session.attributes["questions"][pref_num]
        logging.warning("Current question: " + current_question)
        logging.warning("Next question: " + str(session.attributes["question_number"]))
        return question(current_question)

"""Intent Handlers"""
# Exit if user responds no to getting matched.
@ask.intent("StartIntentNo")
def no_intent():
    bye_text = 'Good bye for now. Come again!'
    return statement(bye_text)

# Ask user for preferences if they would like to get matched.
@ask.intent("StartIntentYes")
def initiate_get_preferences():
    logging.warning("Start Intent Question Number: " + str(session.attributes["question_number"]))
    return get_preference(session.attributes["question_number"])

# Co    ntinue questions until no more are left.
@ask.intent("ContinueIntent")
def next_question():
    logging.warning("Continue Intent Question Number: " + str(session.attributes["question_number"]))
    return get_preference(session.attributes["question_number"])

@ask.intent("LocationIntent", convert={'Location' : str})
def handle_location(Location):
    session.attributes['Location'] = Location
    return question("You selected this location: " + Location + ". Would you like to proceed?")

@ask.intent("SchoolIntent", convert={'School' : str})
def handle_school(School):
    session.attributes['School'] = School
    return question("You are currently attending: " + School + ". Would you like to proceed?")

@ask.intent("GroupSizeIntent", convert={'GroupSize' : str})
def handle_group(GroupSize):
    session.attributes['GroupSize'] = GroupSize
    return question("Your group size is: " + GroupSize + ". Would you like to proceed?")

@ask.intent("PositionIntent", convert={'Position' : str})
def handle_group(Position):
    session.attributes['PositionIntent'] = PositionIntent
    return question("You would like to meet: " + Position + "interns. Is that okay?")

@ask.intent("AgeIntent", convert={'Age' : str})
def handle_group(Age):
    session.attributes['AgeIntent'] = AgeIntent
    return question("Your selected this age group: " + Age + ". Would you like to proceed?")

@ask.intent("HangoutIntent", convert={'Hangout' : str})
def handle_group(Hangout):
    session.attributes['HangoutIntent'] = Hangout
    return question("Your opted to: " + Hangout + ". Would you like to proceed?")

@ask.session_ended
def session_ended():
    return "{}", 200

# Hosted at 127.0.0.1:5000
if __name__ == '__main__':
    app.run(debug=True)
