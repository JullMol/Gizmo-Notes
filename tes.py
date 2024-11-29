from flask import Flask
from threading import Thread
import discord
from discord.ext import commands, tasks
import requests
from dotenv import load_dotenv
import os

FLASK_SERVER_URL = os.getenv("FLASK_SERVER_URL")
FLASK_API_URL = os.getenv('FLASK_API_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Flask App
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask!"

def run_flask():
    app.run(host='0.0.0.0', port=5000)

# Discord Bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is connected!")

@bot.command()
async def hello(ctx):
    if isinstance(ctx.channel, discord.DMChannel):  # Jika perintah diberikan di DM
        await ctx.send(f"Hello, {ctx.author.display_name}!")
    else:  # Jika perintah diberikan di channel publik
        await ctx.send(f"Hello, {ctx.author.display_name}!")
    
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def get_invite(ctx):
    response = requests.get(f"{FLASK_SERVER_URL}/invite-bot")
    if response.status_code == 200:
        invite = response.json()
        await ctx.send(f"Here is your invite link: {invite['invite_link']}")
    else:
        await ctx.send("Failed to get invite link.")

@tasks.loop(count=1)
async def start_flask():
    thread = Thread(target=run_flask)
    thread.start()

# Jalankan Flask saat bot siap
@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready!")
    start_flask.start()

# Jalankan bot
bot.run(BOT_TOKEN)