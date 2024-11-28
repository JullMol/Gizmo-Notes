import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os

load_dotenv('webb\.env')
FLASK_SERVER_URL = os.getenv("FLASK_SERVER_URL")
FLASK_API_URL = os.getenv('FLASK_API_URL')

# URL Flask API

# Ganti dengan token bot Anda
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Inisialisasi bot
intents = discord.Intents.default()
intents.messages = True  # Aktifkan intent pesan
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} telah terhubung!")

@bot.command()
async def hello(ctx):
    try:
        # Bot memanggil API Flask
        response = requests.get(FLASK_API_URL)
        if response.status_code == 200:
            data = response.json()  # Parsing JSON dari Flask
            message = data.get("message", "No message received")
            await ctx.send(message)  # Kirim pesan dari Flask ke Discord
        else:
            await ctx.send("Failed to connect to Flask API.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    
@bot.command()
async def get_invite(ctx):
    response = requests.get(f"{FLASK_SERVER_URL}/invite-bot")
    if response.status_code == 200:
        invite = response.json()
        await ctx.send(f"Here is your invite link: {invite['invite_link']}")
    else:
        await ctx.send("Failed to get invite link.")

# Jalankan bot
bot.run(BOT_TOKEN)