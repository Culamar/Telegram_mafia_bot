import telebot
import datetime
import schedule
import time
from threading import Thread

TOKEN = '' #Bot token
bot = telebot.TeleBot(TOKEN)

# Creating a dictionary to save data
poll_data = {}
counter = {}
poll_message_id = None
# Function to create a poll
def create_poll(chat_id):
    global poll_message_id
    poll = bot.send_poll(chat_id, f'Mafia at Shtolle tomorrow Wednesday ({datetime.date.today()+datetime.timedelta(days=1)})',['Coming at 7:15 PM','Coming at 8 PM','Coming at 9 PM','Coming at 10 PM','Not coming'], False)
    poll_data[poll.poll.id] = {}
    poll_message_id = poll.message_id

# Function to stop poll
def stop_the_poll(chat_id):
    global poll_message_id
    for poll_id in poll_data.keys():
        bot.stop_poll(chat_id, poll_message_id)
    poll_message_id = None
    poll_data.clear()
    # Cleaning dictionaries from data

# Handler to retrieve survey responses
@bot.poll_answer_handler()
def handle_poll_answer(poll_answer):
    poll_id = poll_answer.poll_id
    if poll_id in poll_data:
        if poll_answer.option_ids == []:
            del poll_data[poll_id][poll_answer.user.id]
        elif poll_id in poll_data:
            poll_data[poll_id][poll_answer.user.id] = poll_answer.option_ids


# Function to send a message at what time the mafia will start
def send_vote_count():
    global counter
    for poll_id, data in poll_data.items():
        for id, count in data.items():
            if count[0] in counter.keys():
                counter[count[0]] += 1
            else:
                counter[count[0]] = 1
        if not counter:
            votes_message = 'No mafia today :('
        elif 0 in counter and counter[0] == 6 and 1 in counter and counter[1] >= 1:
            votes_message = 'We are only 6, we can meet at 7:15 pm and play some games till 8 pm. Stolle, prasp. Niezaliežnasci 53, Minsk.'
        elif 0 in counter and counter[0] >= 7:
            votes_message = 'Today meeting will be at 7:15 pm. Stolle, prasp. Niezaliežnasci 53, Minsk.'
        elif (0 in counter and 1 in counter and counter[0]+counter[1] >= 7) or (1 in counter and counter[1] >= 7):
            votes_message = 'Today meeting will be at 8 pm. Stolle, prasp. Niezaliežnasci 53, Minsk.'
        else:
            votes_message = 'No mafia today :('
        bot.send_message('#Chat id', votes_message)
        # Cleaning dictionaries from data
        counter = {}


# Schedule to create a survey every Tuesday
schedule.every().tuesday.at("08:02").do(create_poll, chat_id='#Chat id')

# Schedule for sending message
schedule.every().wednesday.at("14:30").do(send_vote_count)

# Schedule to stop poll
schedule.every().wednesday.at("16:00").do(stop_the_poll, chat_id='#Chat id')

# Function to run the schedule
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start thread for schedule
Thread(target=run_schedule).start()

# Start the bot
bot.polling(non_stop=True)

