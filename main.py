import os
import discord
from discord.ext import commands
from flask import Flask, request, jsonify
from threading import Thread
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
PORT = int(os.getenv('PORT', 5000))

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Flask App Setup
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    # Extract task info (customize based on your website's payload)
    task_title = data.get('title', 'New Task')
    task_description = data.get('description', 'No description provided')
    task_url = data.get('url', '')

    message = f"🆕 **New Task Posted!**\n\n**Title:** {task_title}\n**Description:** {task_description}"
    if task_url:
        message += f"\n**Link:** {task_url}"

    # Send message to Discord
    if CHANNEL_ID and CHANNEL_ID.isdigit():
        async def send_to_discord():
            try:
                channel = bot.get_channel(int(CHANNEL_ID)) or await bot.fetch_channel(int(CHANNEL_ID))
                if channel:
                    await channel.send(message)
                else:
                    print(f"Error: Channel {CHANNEL_ID} not found.")
            except Exception as e:
                print(f"Error sending to Discord: {e}")

        # Use bot.loop to run the coroutine from the Flask thread
        asyncio.run_coroutine_threadsafe(send_to_discord(), bot.loop)
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "DISCORD_CHANNEL_ID is not set or invalid"}), 500

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start Discord Bot
    if TOKEN and TOKEN != "your_token_here":
        bot.run(TOKEN)
    else:
        print("Please set your DISCORD_TOKEN in the .env file")
