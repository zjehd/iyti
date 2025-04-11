from flask import Flask, request, jsonify
import subprocess
import threading
import time
from telegram import Bot

app = Flask(__name__)

BOT_TOKEN = "your-telegram-bot-token"
bot = Bot(token=BOT_TOKEN)

# This function will run commands received from the frontend
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

# Background task to keep the Telegram bot running
def start_bot():
    while True:
        bot.send_message(chat_id='your-chat-id', text="Bot is running...")
        time.sleep(60)

# Starting the bot in a separate thread
bot_thread = threading.Thread(target=start_bot)
bot_thread.start()

@app.route('/run_command', methods=['POST'])
def handle_command():
    data = request.get_json()
    command = data.get('command')
    if command:
        output = run_command(command)
        return jsonify({'output': output})
    return jsonify({'output': 'No command received'})

if __name__ == '__main__':
    app.run(debug=True)
