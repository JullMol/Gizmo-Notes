from flask import Flask
from threading import Thread
import discord
from discord.ext import commands, tasks
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path='d:/PYTHON/Project/Gizmo-Notes/.env')

FLASK_SERVER_URL = os.getenv("FLASK_SERVER_URL")
FLASK_API_URL = os.getenv("FLASK_API_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Bot token is missing! Please check your .env file.")

# Flask App
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask!"

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Discord Bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Flask thread check
flask_thread_started = False

@bot.event
async def on_ready():
    global flask_thread_started
    print(f"Bot {bot.user} is ready!")
    if not flask_thread_started:
        flask_thread_started = True
        thread = Thread(target=run_flask)
        thread.start()

@bot.command()
async def hello(ctx):
    if isinstance(ctx.channel, discord.DMChannel):  # Command issued in DM
        await ctx.send(f"Hello, {ctx.author.display_name}!")
    else:  # Command issued in public channel
        await ctx.send(f"Hello, {ctx.author.display_name}!")
    
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def get_invite(ctx):
    try:
        response = requests.get(f"{FLASK_SERVER_URL}/invite-bot")
        if response.status_code == 200:
            invite = response.json()
            await ctx.send(f"Here is your invite link: {invite['invite_link']}")
        else:
            await ctx.send("Failed to get invite link.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

# Run the bot
bot.run(BOT_TOKEN)