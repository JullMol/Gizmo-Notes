from flask import Flask
from threading import Thread
import discord
from discord.ext import commands, tasks
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

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
async def create_gp(ctx, category_name: str, *, default_channel_name: str = None):
    guild = ctx.guild
    author = ctx.author

    # Format nama kategori dan channel default
    formatted_category_name = category_name.strip()
    formatted_channel_name = default_channel_name.lower().replace(" ", "-") if default_channel_name else f"{formatted_category_name.lower().replace(' ', '-')}-projects"

    # Periksa apakah kategori sudah ada
    existing_category = discord.utils.get(guild.categories, name=formatted_category_name)
    if existing_category:
        await ctx.send(f"Kategori **{formatted_category_name}** sudah ada!")
        return

    # Membuat kategori baru
    try:
        new_category = await guild.create_category(formatted_category_name)
        await ctx.send(f"Kategori **{new_category.name}** berhasil dibuat!")

        # Mengatur izin khusus untuk channel default
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),  # Semua anggota tidak bisa membaca
            author: discord.PermissionOverwrite(read_messages=True)  # Pembuat kategori bisa membaca
        }

        # Membuat channel default di dalam kategori baru
        new_channel = await guild.create_text_channel(
            formatted_channel_name, category=new_category, overwrites=overwrites
        )
        await ctx.send(
            f"Channel default **{new_channel.name}** berhasil dibuat di kategori **{new_category.name}**!\n"
            f"Link: https://discord.com/channels/{guild.id}/{new_channel.id}"
        )
    except discord.Forbidden:
        await ctx.send("Saya tidak memiliki izin untuk membuat kategori atau channel!")
    except discord.HTTPException as e:
        await ctx.send(f"Terjadi kesalahan: {e}")
            
@bot.command()
async def add_gp(ctx, category_name: str, *, channel_name: str):
    guild = ctx.guild
    author = ctx.author

    # Format nama kategori dan channel
    formatted_category_name = category_name.strip()
    formatted_channel_name = channel_name.lower().replace(" ", "-")

    # Temukan kategori berdasarkan nama
    category = discord.utils.get(guild.categories, name=formatted_category_name)
    if not category:
        await ctx.send(f"Kategori **{formatted_category_name}** tidak ditemukan!")
        return

    # Tentukan nama channel default (ini bisa disesuaikan dengan nama yang diberikan oleh pengguna)
    default_channel_name = f"{formatted_category_name.lower().replace(' ', '-')}-projects"  # Misalnya: gp-projects

    # Temukan channel default dalam kategori
    default_channel = discord.utils.get(category.text_channels, name=default_channel_name)

    # Pastikan perintah dijalankan di channel default
    if ctx.channel != default_channel:
        await ctx.send(f"Perintah ini hanya bisa dijalankan di channel default **{default_channel_name}**!")
        return

    # Cek apakah channel sudah ada dalam kategori
    existing_channel = discord.utils.get(category.channels, name=formatted_channel_name)
    if existing_channel:
        await ctx.send(f"Channel **{formatted_channel_name}** sudah ada di kategori **{category.name}**!")
        return

    # Membuat channel baru di dalam kategori
    try:
        new_channel = await guild.create_text_channel(formatted_channel_name, category=category)
        await ctx.send(f"Channel **{new_channel.name}** berhasil dibuat di kategori **{category.name}**!")
    except discord.Forbidden:
        await ctx.send("Saya tidak memiliki izin untuk membuat channel!")
    except discord.HTTPException as e:
        await ctx.send(f"Terjadi kesalahan saat membuat channel: {e}")
            
@bot.command()
async def link(ctx, *, category_name: str):
    guild = ctx.guild

    # Temukan kategori berdasarkan nama
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        await ctx.send(f"Kategori **{category_name}** tidak ditemukan!")
        return

    # Dapatkan semua channel dalam kategori
    if category.channels:
        channel_links = [
            f"[{channel.name}](https://discord.com/channels/{guild.id}/{channel.id})"
            for channel in category.channels
        ]
        await ctx.send(
            f"Channel dalam kategori **{category.name}**:\n" + "\n".join(channel_links)
        )
    else:
        await ctx.send(f"Kategori **{category.name}** tidak memiliki channel!")

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