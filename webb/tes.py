from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

FLASK_SERVER_URL = os.getenv("FLASK_SERVER_URL")
FLASK_API_URL = os.getenv("FLASK_API_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
personal_bot = os.getenv("personal_bot_link")

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

admins = {}
roles = {}
emails = {}

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
    await ctx.send(
        "Hello! I am your personal bot. Here are the commands you can use:\n"
        "1. !ping: Test bot\n"
        "2. !create_gp <category_name> : Create default category and channel\n"
        "3. !add_gp <category_name> <channel_name> : Add channel to category\n"
        "4. !role : View role\n"
        "5. !pick_role <role_name> : Select role\n"
        "6. !add_meet <category _name> <voice_channel_name> : Create voice channel\n"
        "7. !record <channel_name> <voice_channel_name> : Record activity\n"
        "8. !get_record : Request the recording result\n"
        "9. !end_gp : Delete category"
    )
    
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
        await ctx.send(f"Category with named **{formatted_category_name}** is already!")
        return

    # Membuat kategori baru
    try:
        new_category = await guild.create_category(formatted_category_name)
        await ctx.send(f"Category with named**{new_category.name}** successfully created!")

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
            f"Default Channel with named **{new_channel.name}** created successfully in Category named **{new_category.name}**!\n"
            f"Link: https://discord.com/channels/{guild.id}/{new_channel.id}"
        )
    except discord.Forbidden:
        await ctx.send("I don't have permission to create categories or channels!")
    except discord.HTTPException as e:
        await ctx.send(f"Something error: {e}")
            
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
        await ctx.send(f"Category with named **{formatted_category_name}** not found!")
        return

    # Tentukan nama channel default (ini bisa disesuaikan dengan nama yang diberikan oleh pengguna)
    default_channel_name = f"{formatted_category_name.lower().replace(' ', '-')}-projects"  # Misalnya: gp-projects

    # Temukan channel default dalam kategori
    default_channel = discord.utils.get(category.text_channels, name=default_channel_name)

    # Pastikan perintah dijalankan di channel default
    if ctx.channel != default_channel:
        await ctx.send(f"This command can only be run on the default channel **{default_channel_name}**!")
        return

    # Cek apakah channel sudah ada dalam kategori
    existing_channel = discord.utils.get(category.channels, name=formatted_channel_name)
    if existing_channel:
        await ctx.send(f"Channel with named **{formatted_channel_name}** is already in Category Named **{category.name}**!")
        return

    # Membuat channel baru di dalam kategori
    try:
        new_channel = await guild.create_text_channel(formatted_channel_name, category=category)
        await ctx.send(f"Channel with named **{new_channel.name}** created successfully in Category named **{category.name}**!")
    except discord.Forbidden:
        await ctx.send("I don't have permission to create channels!")
    except discord.HTTPException as e:
        await ctx.send(f"Something error: {e}")
            
@bot.command()
async def link(ctx, *, category_name: str):
    guild = ctx.guild

    # Temukan kategori berdasarkan nama
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        await ctx.send(f"Category with named **{category_name}** not found!")
        return

    # Dapatkan semua channel dalam kategori
    if category.channels:
        channel_links = [
            f"[{channel.name}](https://discord.com/channels/{guild.id}/{channel.id})"
            for channel in category.channels
        ]
        await ctx.send(
            f"Channel in Category **{category.name}**:\n" + "\n".join(channel_links)
        )
    else:
        await ctx.send(f"Category with named **{category.name}** not have channel!")
        
@bot.command()
async def add_meet(ctx, category_name: str, *, voice_channel_name: str):
    guild = ctx.guild
    author = ctx.author

    # Format nama kategori dan voice channel
    formatted_category_name = category_name.strip()
    formatted_voice_channel_name = voice_channel_name.lower().replace(" ", "-")

    # Temukan kategori berdasarkan nama
    category = discord.utils.get(guild.categories, name=formatted_category_name)
    if not category:
        await ctx.send(f"Category with named **{formatted_category_name}** not found!")
        return

    # Tentukan nama channel default
    default_channel_name = f"{formatted_category_name.lower().replace(' ', '-')}-projects"  # Misalnya: gp-projects

    # Temukan channel default dalam kategori
    default_channel = discord.utils.get(category.text_channels, name=default_channel_name)

    # Pastikan perintah dijalankan di channel default
    if ctx.channel != default_channel:
        await ctx.send(f"This command can only be run on the default channel **{default_channel_name}**!")
        return

    # Cek apakah voice channel sudah ada dalam kategori
    existing_channel = discord.utils.get(category.voice_channels, name=formatted_voice_channel_name)
    if existing_channel:
        await ctx.send(f"Voice channel **{formatted_voice_channel_name}** is already in Category **{category.name}**!")
        return

    # Membuat voice channel baru di dalam kategori
    try:
        new_voice_channel = await guild.create_voice_channel(formatted_voice_channel_name, category=category)
        await ctx.send(f"Voice channel **{new_voice_channel.name}** created successfully in Category named **{category.name}**!")
    except discord.Forbidden:
        await ctx.send("I don't have permission to create voice channels!")
    except discord.HTTPException as e:
        await ctx.send(f"Something error: {e}")

        
@bot.command()
async def end_gp(ctx, *, category_name: str):
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        await ctx.send(f"Category with named **{category_name}** not found!")
        return

    try:
        for channel in category.channels:
            await channel.delete()
        await category.delete()
        await ctx.send(f"Category **{category_name}** successfully deleted along with all channels in it!")
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete categories or channels!")
    except discord.HTTPException as e:
        await ctx.send(f"Something error: {e}")

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