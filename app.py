# package imports
from flask import Flask
from gs_bot import GSheetsBot
from fb_messenger import FbMessenger, Event

# setup of the environment variables, we will fill them later with values
FACEBOOK_VERIFY_TOKEN = 'cndjnclkjsancdjnalsjcn'
FACEBOOK_PAGE_ACCESS_TOKEN = 'EAAZAmp8KZCvKUBAHcRqcX3wTGXcVDV41ow0XFXRmzlbhQ8ZAtOZBqbLEBh2Yv9WMde0r3t5NRSDikS4YAhmiXIedeUvve6TXQKniJ9pg4ziy0RNBP7frHOW7ikfZBMU1JLYRFmDV8ybez64Sk428ENXMyLXi3UoaZCo5e3rcRn8ON3uFYIBtQw'
FACEBOOK_ROUTE = '/'
GOOGLE_CREDENTIALS_PATH = 'chatbot-test-199f21257d88.json'
GOOGLE_SPREADSHEET_NAME = 'chatbot1234'
GOOGLE_SPREADSHEET_PAGE = 0
STATE = 0
SCORE = 0


#"How are you feeling?"
#"How well did you sleep last night?"
#"How much time did you spend with family or friends?"
#"How much water did you drink today?"
#"How balanced was your diet today?"
#"How active were you today?"
#"How productive were you today?"
#"How relaxed do you feel today?"

# then create a Flask app
app = Flask('bot')

# enable the connection interface with Facebook
messenger_interface = FbMessenger(app, FACEBOOK_ROUTE, FACEBOOK_VERIFY_TOKEN, FACEBOOK_PAGE_ACCESS_TOKEN)

# enable the connection interface with Google SpreadSheet, which will contain the bot's flow
bot = GSheetsBot(app, GOOGLE_CREDENTIALS_PATH, GOOGLE_SPREADSHEET_NAME, GOOGLE_SPREADSHEET_PAGE)

# Now define a custom reply function for the Facebook messenger interface to take into account the bot in the spreadsheet
def reply(e: Event):
    print(e.content['text'])
    if e.content['text'] == 'hi':
        e.reply({'text': 'Hello!'})
        e.reply({'text': 'How are you feeling?'})
        #STATE = STATE + 1
        #print(STATE)
    if e.content['text'] == 'good':
        e.reply({'text': 'How well did you sleep last night'})
    if e.content['text'] == 'not good':
        e.reply({'text': 'How well did you sleep last night'})
    if e.content['text'] == 'well':
        e.reply({'text': 'How much time did you spend with family or friends?'})
    if e.content['text'] == 'not well':
        e.reply({'text': 'How much time did you spend with family or friends?'})
    if e.content['text'] == 'a lot':
        e.reply({'text': 'How much water did you drink today?'})
    if e.content['text'] == 'not a lot':
        e.reply({'text': 'How much water did you drink today?'})
    if e.content['text'] == 'a lot of water':
        e.reply({'text': 'How balanced was your diet today?'})
    if e.content['text'] == 'not a lot of water':
        e.reply({'text': 'How balanced was your diet today?'})
    if e.content['text'] == 'balanced':
        e.reply({'text': 'How active were you today?'})
    if e.content['text'] == 'not balanced':
        e.reply({'text': 'How active were you today?'})
    if e.content['text'] == 'active':
        e.reply({'text': 'You should stay hydrated.'})
    if e.content['text'] == 'not active':
        e.reply({'text': 'You dont seem to be very active, maybe you should try some yoga.'})

    if e.content['text'] == 'help':
        e.reply({'text': 'This is the keep appy chatbot. It will help you with youre mental health.'})
        e.reply({'text': 'Say hi to initialise a chat and answer the questions given.'})


    #if e.content['text'] == 'good':
    #    e.reply({'text' : 'Excellent'})
    #else:
    #    e.reply({'text': 'sorry I didnt quite get that'})
    #responses = bot.reply_graph(e.sender_id, e.content['text'])
    #for response in responses:
    #    e.reply(response)

# setup the reply funtion above as the callback for the message event listener of the messenger_interface
messenger_interface.callback_manager.set_callback(reply, 'message')

# and run the app !
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
