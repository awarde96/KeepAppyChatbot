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

# then create a Flask app
app = Flask('bot')

# enable the connection interface with Facebook
messenger_interface = FbMessenger(app, FACEBOOK_ROUTE, FACEBOOK_VERIFY_TOKEN, FACEBOOK_PAGE_ACCESS_TOKEN)

# enable the connection interface with Google SpreadSheet, which will contain the bot's flow
bot = GSheetsBot(app, GOOGLE_CREDENTIALS_PATH, GOOGLE_SPREADSHEET_NAME, GOOGLE_SPREADSHEET_PAGE)

# Now define a custom reply function for the Facebook messenger interface to take into account the bot in the spreadsheet
def reply(e: Event):
    print('fuckkkkkkkkkkkkkkkkkkkkkkk')
    e.reply({'text': 'hello world !'})
    #responses = bot.reply_graph(e.sender_id, e.content['text'])
    #for response in responses:
    #    e.reply(response)

# setup the reply funtion above as the callback for the message event listener of the messenger_interface
messenger_interface.callback_manager.set_callback(reply, 'message')

# and run the app !
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
