import discord
from discord.ext import commands, tasks
from discord.utils import get
from flask import Flask
from threading import Thread
import asyncio
import requests
import wave
import subprocess
from dotenv import load_dotenv
import os
from fpdf import FPDF
import csv
from datetime import datetime
from database import Member, Record, Users, db
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

# Load environment variables
load_dotenv()

FLASK_SERVER_URL = os.getenv("FLASK_SERVER_URL")
FLASK_API_URL = os.getenv("FLASK_API_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
personal_bot = os.getenv("personal_bot_link")
sender_email = os.getenv("GMAIL_EMAIL")
sender_password = os.getenv("GMAIL_PASSWORD")

if not BOT_TOKEN:
    raise ValueError("Bot token is missing! Please check your .env file.")

path_db = os.path.join(os.getcwd(), 'instance/pythonanywhere')

# Flask App
app = Flask(__name__, instance_path= path_db)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path,'local_database.db')}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def home():
    return "Hello from Flask!"

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Discord Bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.voice_states = True
global bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Flask thread check
flask_thread_started = False

admins = {}
roles = {}
emails = {}
recording_status = False
recording_channel = None
MAX_RECORD_DURATION = 5 * 60
is_recording = False
voice_client = None
recording_data = []

def download_database():
    url = 'https://gizmonote.pythonanywhere.com/static/local_database.db'

    response = requests.get(url)

    if response.status_code == 200:
        with open(f'{path_db}/local_database.db', 'wb') as file:
            file.write(response.content)

        print('Database downloaded successfully.')
    else:
        print('Failed to download the database.')
        
@bot.event
async def on_member_update(before, after):
    guild = after.guild
    channel_name = "bot_testing"

    # Temukan channel bot_testing
    channel = discord.utils.get(guild.text_channels, name=channel_name)
    if not channel:
        print(f"Channel **{channel_name}** not found!")
        return

    # Bersihkan semua pesan di channel
    try:
        await channel.purge()
        print(f"Message on channel **{channel_name}** deleted.")
    except discord.Forbidden:
        print("Bot does not have permission to delete messages.")
    except discord.HTTPException as e:
        print(f"An error occurred while deleting a message: {e}")

@bot.command()
async def clear(ctx):
    await ctx.channel.purge()
    await ctx.send("🧹 Channel has been cleared!")

@bot.event
async def on_member_join(member):
    guild = member.guild
    channel_name = "bot_testing"  # Ganti dengan nama channel yang ingin Anda bersihkan

    # Temukan channel bot_testing
    channel = discord.utils.get(guild.text_channels, name=channel_name)
    if not channel:
        print(f"Channel **{channel_name}** not found!")
        return

    # Bersihkan semua pesan di channel
    try:
        await channel.purge()
        await channel.send(f"Welcome to Gizmo GP Server, {member.mention}!")
    except discord.Forbidden:
        print("Bot not have permission.")
    except discord.HTTPException as e:
        print(f"Something error: {e}")

@bot.event
async def on_ready():
    global flask_thread_started
    print(f"🤖 Bot {bot.user} is ready!")
    if not flask_thread_started:
        flask_thread_started = True
        thread = Thread(target=run_flask)
        thread.start()

@bot.command()
async def hello(ctx):
    if isinstance(ctx.channel, discord.DMChannel):  # Command issued in DM
        await ctx.send(f"👋 Hello {ctx.author.display_name}!\n🤖I'm Bot Gizmo GP, you can get information about the instruction if you send me\n\n```!ping```\n")
    else:  # Command issued in public channel
        await ctx.send(f"👋 Hello {ctx.author.display_name}!,\n🤖I'm Bot Gizmo GP, you can get information about the instruction if you send me\n\n```!ping```\n")
    
@bot.command()
async def ping(ctx):
    await ctx.send(
        "🔔 Hello! I am your personal bot Gizmo GP. Here are the commands you can use: 🚀\n"
        "1️⃣ !get_id <email_user_login> : 🔍 Get information about user_id for !get_email and !email_invite\n"
        "2️⃣ !get_email <user_id>: 📧 Get email about a member\n"
        "3️⃣ !create_gp <category_name> : 🏗️ Create default category and channel\n"
        "4️⃣ !add_gp <category_name> <channel_name> : ➕ Add channel to category\n"
        "5️⃣ !add_meet <category_name> <voice_channel_name> : 🎙️ Create voice channel\n"
        "6️⃣ !email_invite <channel_name> <user_id> : ✉️ Send email invitation to all members\n"
        "7️⃣ !role : 🧑‍💼 View available roles\n"
        "8️⃣ !pick_role <role_name> : 🎭 Select a role\n"
        "9️⃣ !change_role <@Username> <role_name> : 🔄 Change another member's role (Admin only)\n"
        "🔟 !start_text <category_name> <channel_name> : 📝 Record activity in a text channel\n"
        "1️⃣1️⃣ !stop_text <category_name> <channel_name> : 🛑 Stop recording in a text channel\n"
        "1️⃣2️⃣ !convert_and_upload <channel_name> : 🔄 Convert CSV files to PDF and upload to AnonFiles\n"
        "1️⃣3️⃣ !start_voice <category_name> <voice_channel_name> : 🎙️ Record activity in a voice channel\n"
        "1️⃣4️⃣ !stop_voice <category_name> <voice_channel_name> : 🛑 Stop recording in a voice channel\n"
        "1️⃣5️⃣ !end_gp <category_name> : 🗑️ Delete a category\n"
        "1️⃣6️⃣ !clear : 🧹 Clear channel history"
    )
    
@bot.command()
async def get_id(ctx, email: str):
    try:
        download_database()
        with app.app_context():
            # Query user berdasarkan email
            user = Users.query.filter_by(email=email).first()

            if user:
                # Kirim data user_id, username, dan email
                await ctx.send(
                    f"📋 User Info:\n"
                    f"User ID: `{user.id}`\n"
                    f"Username: `{user.username}`\n"
                    f"Email: `{user.email}`"
                )
            else:
                # Jika email tidak ditemukan
                await ctx.send(f"❌ No user found with email `{email}`.")
    except Exception as e:
        # Tangkap dan kirim error
        await ctx.send(f"❌ An error occurred while retrieving user data: {str(e)}")
    
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
        await ctx.send(f"🏗️ Category with named **{formatted_category_name}** is already!")
        return

    # Membuat kategori baru
    try:
        new_category = await guild.create_category(formatted_category_name)
        await ctx.send(f"🏗️ Category with named**{new_category.name}** successfully created!")

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
            f"🌐 Default Channel with named **{new_channel.name}** created successfully in Category named **{new_category.name}**!\n"
            f"Link: https://discord.com/channels/{guild.id}/{new_channel.id}"
        )
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to create categories or channels!")
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
        await ctx.send(f"❌ Category with named **{formatted_category_name}** not found!")
        return

    # Tentukan nama channel default (ini bisa disesuaikan dengan nama yang diberikan oleh pengguna)
    default_channel_name = f"{formatted_category_name.lower().replace(' ', '-')}-projects"  # Misalnya: gp-projects

    # Temukan channel default dalam kategori
    default_channel = discord.utils.get(category.text_channels, name=default_channel_name)

    # Pastikan perintah dijalankan di channel default
    if ctx.channel != default_channel:
        await ctx.send(f"❌ This command can only be run on the default channel **{default_channel_name}**!")
        return

    # Cek apakah channel sudah ada dalam kategori
    existing_channel = discord.utils.get(category.channels, name=formatted_channel_name)
    if existing_channel:
        await ctx.send(f"➕ Channel with named **{formatted_channel_name}** is already in Category Named **{category.name}**!")
        return

    # Membuat channel baru di dalam kategori
    try:
        new_channel = await guild.create_text_channel(formatted_channel_name, category=category)
        await ctx.send(f"➕ Channel with named **{new_channel.name}** created successfully in Category named **{category.name}**!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to create channels!")
    except discord.HTTPException as e:
        await ctx.send(f"Something error: {e}")
            
@bot.command()
async def link(ctx, *, category_name: str):
    guild = ctx.guild

    # Temukan kategori berdasarkan nama
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        await ctx.send(f"❌ Category with named **{category_name}** not found!")
        return

    # Dapatkan semua channel dalam kategori
    if category.channels:
        channel_links = [
            f"[{channel.name}](https://discord.com/channels/{guild.id}/{channel.id})"
            for channel in category.channels
        ]
        await ctx.send(
            f"🌐 Channel in Category **{category.name}**:\n" + "\n".join(channel_links)
        )
    else:
        await ctx.send(f"🌐 Category with named **{category.name}** not have channel!")
        
@bot.command()
async def role(ctx):
    guild = ctx.guild

    # Daftar role yang akan ditampilkan
    role_names = ["Admin", "Member", "Guest"]

    # Periksa apakah role-role tersebut ada di server
    available_roles = [role.name for role in guild.roles if role.name in role_names]
    if not available_roles:
        await ctx.send("❌ There are no roles available on this server!")
        return

    # Kirim daftar role ke user
    await ctx.send(f"🧑‍💼 Available Roles: {', '.join(available_roles)}")


@bot.command()
async def pick_role(ctx, *, role_name: str):
    guild = ctx.guild
    member = ctx.author

    # Periksa apakah role ada di server
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        await ctx.send(f"❌ Role **{role_name}** not found! Use `!role` to view the list of available roles.")
        return

    # Periksa apakah user sudah memiliki role tersebut
    if role in member.roles:
        await ctx.send(f"🎭 You already have a role **{role_name}**!")
        return

    # Hapus role lain sebelum menambahkan role baru
    role_names = ["Admin", "Member", "Guest"]
    roles_to_remove = [r for r in member.roles if r.name in role_names]

    try:
        # Hapus role-role lama
        for old_role in roles_to_remove:
            await member.remove_roles(old_role)

        # Tambahkan role baru
        await member.add_roles(role)
        await ctx.send(f"🎭 Your role has been updated to **{role_name}**!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to change your role!")
    except discord.HTTPException as e:
        await ctx.send(f"Something error: {e}")

@bot.command()
@commands.has_role("Admin")  # Hanya bisa dijalankan oleh user dengan role "Admin"
async def change_role(ctx, member: discord.Member, *, role_name: str):
    guild = ctx.guild

    # Daftar role yang diizinkan
    allowed_roles = ["Admin", "Member", "Guest"]

    # Validasi role
    role = discord.utils.get(guild.roles, name=role_name)
    if not role or role_name not in allowed_roles:
        await ctx.send(f"❌ Role **{role_name}** invalid! Available roles: {', '.join(allowed_roles)}")
        return

    # Periksa apakah member sudah memiliki role tersebut
    if role in member.roles:
        await ctx.send(f"🎭 Member **{member.display_name}** already have a role **{role_name}**!")
        return

    # Hapus role lama (jika ada) sebelum menambahkan role baru
    roles_to_remove = [r for r in member.roles if r.name in allowed_roles]

    try:
        # Hapus role lama
        for old_role in roles_to_remove:
            await member.remove_roles(old_role)

        # Tambahkan role baru
        await member.add_roles(role)
        await ctx.send(f"🎭 Member role **{member.display_name}** has been changed to **{role_name}** by **{ctx.author.display_name}**.")
    except discord.Forbidden:
        await ctx.send("❌ I do not have permission to change this member role!")
    except discord.HTTPException as e:
        await ctx.send(f"Something error: {e}")
        
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
        await ctx.send(f"❌ Category with named **{formatted_category_name}** not found!")
        return

    # Tentukan nama channel default
    default_channel_name = f"{formatted_category_name.lower().replace(' ', '-')}-projects"  # Misalnya: gp-projects

    # Temukan channel default dalam kategori
    default_channel = discord.utils.get(category.text_channels, name=default_channel_name)

    # Pastikan perintah dijalankan di channel default
    if ctx.channel != default_channel:
        await ctx.send(f"❌ This command can only be run on the default channel **{default_channel_name}**!")
        return

    # Cek apakah voice channel sudah ada dalam kategori
    existing_channel = discord.utils.get(category.voice_channels, name=formatted_voice_channel_name)
    if existing_channel:
        await ctx.send(f"➕ Voice channel **{formatted_voice_channel_name}** is already in Category **{category.name}**!")
        return

    # Membuat voice channel baru di dalam kategori
    try:
        new_voice_channel = await guild.create_voice_channel(formatted_voice_channel_name, category=category)
        await ctx.send(f"➕ Voice channel **{new_voice_channel.name}** created successfully in Category named **{category.name}**!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to create voice channels!")
    except discord.HTTPException as e:
        await ctx.send(f"Something error: {e}")

@bot.command()
async def start_text(ctx, category_name: str, *, channel_name: str):
    guild = ctx.guild

    # Format nama kategori dan channel
    formatted_category_name = category_name.strip()
    formatted_channel_name = channel_name.lower().replace(" ", "-")

    # Temukan kategori berdasarkan nama
    category = discord.utils.get(guild.categories, name=formatted_category_name)
    if not category:
        await ctx.send(f"❌ Category with named **{formatted_category_name}** not found!")
        return

    # Tentukan nama channel default
    default_channel_name = f"{formatted_category_name.lower().replace(' ', '-')}-projects"

    # Temukan channel default dalam kategori
    default_channel = discord.utils.get(category.text_channels, name=default_channel_name)

    # Validasi: Perintah hanya dijalankan di channel default
    if ctx.channel != default_channel:
        await ctx.send(f"❌ This command can only be run on the default channel **{default_channel_name}**!")
        return

    # Simpan status perekaman
    global recording_status, recording_channel
    recording_status = True
    recording_channel = formatted_channel_name
    await ctx.send(f"✅ Recording started for channel **{formatted_channel_name}** in category **{formatted_category_name}**.")

@bot.command()
async def stop_text(ctx, category_name: str, *, channel_name: str):
    guild = ctx.guild

    # Format nama kategori dan channel
    formatted_category_name = category_name.strip()
    formatted_channel_name = channel_name.lower().replace(" ", "-")

    # Temukan kategori berdasarkan nama
    category = discord.utils.get(guild.categories, name=formatted_category_name)
    if not category:
        await ctx.send(f"❌ Category with named **{formatted_category_name}** not found!")
        return

    # Tentukan nama channel default
    default_channel_name = f"{formatted_category_name.lower().replace(' ', '-')}-projects"

    # Temukan channel default dalam kategori
    default_channel = discord.utils.get(category.text_channels, name=default_channel_name)

    # Validasi: Perintah hanya dijalankan di channel default
    if ctx.channel != default_channel:
        await ctx.send(f"❌ This command can only be run on the default channel **{default_channel_name}**!")
        return

    # Hentikan perekaman
    global recording_status, recording_channel
    if recording_status and recording_channel == formatted_channel_name:
        recording_status = False
        recording_channel = None
        await ctx.send(f"✅ Recording stopped for channel **{formatted_channel_name}** in category **{formatted_category_name}**.")
    else:
        await ctx.send("❌ No recording is currently active.")

@bot.event
async def on_message(message):
    global recording_status, recording_channel

    # Abaikan pesan dari bot itu sendiri
    if message.author.bot:
        return

    # Rekam pesan jika perekaman aktif dan channel sesuai
    if recording_status and message.channel.name == recording_channel:
        filename = f"{recording_channel}_record.csv"
        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([message.author.name, message.content, message.created_at])

    await bot.process_commands(message)

@bot.command()
async def convert_and_upload(ctx, category_name: str, *, channel_name: str):
    guild = ctx.guild

    # Format nama kategori dan channel
    formatted_category_name = category_name.strip()
    formatted_channel_name = channel_name.lower().replace(" ", "-")

    # Temukan kategori berdasarkan nama
    category = discord.utils.get(guild.categories, name=formatted_category_name)
    if not category:
        await ctx.send(f"❌ Category with named **{formatted_category_name}** not found!")
        return

    # Tentukan nama channel default
    default_channel_name = f"{formatted_category_name.lower().replace(' ', '-')}-projects"

    # Temukan channel default dalam kategori
    default_channel = discord.utils.get(category.text_channels, name=default_channel_name)

    # Validasi: Perintah hanya dijalankan di channel default
    if ctx.channel != default_channel:
        await ctx.send(f"❌ This command can only be run on the default channel **{default_channel_name}**!")
        return

    # Konversi CSV ke PDF
    csv_filename = f"{formatted_channel_name}_record.csv"
    pdf_filename = f"{formatted_channel_name}_record.pdf"

    try:
        csv_to_pdf(csv_filename, pdf_filename)
    except FileNotFoundError:
        await ctx.send(f"❌ CSV file `{csv_filename}` not found. Ensure recording was started for this channel.")
        return

    # Upload file PDF to AnonFiles
    result = upload_to_gofiles(pdf_filename)
    await ctx.send(result)

def csv_to_pdf(csv_filename, pdf_filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    #Set Title Column
    pdf.set_font("Arial", "B" ,size=12)
    pdf.cell(40, 10, "Author", border=1, align="C")
    pdf.cell(100, 10, "Content", border=1, align="C")
    pdf.cell(40, 10, "Timestamp", border=1, align="C")
    pdf.ln()
    
    #Set font
    pdf.set_font("Arial", "", 10)

    with open(csv_filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            author, content, timestamp = row
            
            try:
                timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f+00:00")
                timestamp = timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")  # Format yang lebih bersih
            except ValueError:
                pass
            
            content = content[:150] + '...' if len(content) > 150 else content  # Truncate jika terlalu panjang

            pdf.cell(40, 10, author, border=1, align="C")
            pdf.cell(100, 10, content, border=1, align="C")
            pdf.cell(40, 10, timestamp, border=1, align="C")
            pdf.ln()

    pdf.output(pdf_filename)

def upload_to_gofiles(filename):
    try:
        with open(filename, "rb") as f:
            response = requests.post("https://store1.gofile.io/uploadFile", files={"file": f}, verify=False)
            if response.status_code != 200:
                return f"Failed to upload. HTTP Status Code: {response.status_code}"
            
            data = response.json()
            if data["status"] == "ok":
                file_url = data["data"]["downloadPage"]
                return f"File uploaded successfully to GoFiles!\nLink: {file_url}"
            else:
                return f"Failed to upload file: {data.get('error', {}).get('message', 'Unknown error')}"
    except FileNotFoundError:
        return f"File `{filename}` not found!"
    except Exception as e:
        return f"An error occurred: {e}"
    
# Command: Rekam Voice Channel
@bot.command()
async def start_voice(ctx, category_name: str, *, voice_channel_name: str):
    global is_recording, recording_data, voice_client

    if is_recording:
        await ctx.send("❌ Recording is in progress. Use `!stop_record_voice` to stop.")
        return

    guild = ctx.guild
    channel = discord.utils.get(guild.voice_channels, name=voice_channel_name)
    
    # Format nama kategori dan channel
    formatted_category_name = category_name.strip()
    formatted_voice_channel_name = voice_channel_name.lower().replace(" ", "-")

    # Temukan kategori berdasarkan nama
    category = discord.utils.get(guild.categories, name=formatted_category_name)
    if not category:
        await ctx.send(f"❌ Category with named **{formatted_category_name}** not found!")
        return

    # Tentukan nama channel default
    default_channel_name = f"{formatted_category_name.lower().replace(' ', '-')}-projects"

    # Temukan channel default dalam kategori
    default_channel = discord.utils.get(category.text_channels, name=default_channel_name)

    # Validasi: Perintah hanya dijalankan di channel default
    if ctx.channel != default_channel:
        await ctx.send(f"❌ This command can only be run on the default channel **{default_channel_name}**!")
        return
    
    # Cek apakah channel sudah ada dalam kategori
    existing_channel = discord.utils.get(category.channels, name=formatted_voice_channel_name)
    if existing_channel:
        await ctx.send(f"✅ Channel with named **{formatted_voice_channel_name}** is already in Category Named **{category.name}**!")
        return

    if not channel:
        await ctx.send(f"❌ Voice channel **{voice_channel_name}** is not found!")
        return

    try:
        # Hubungkan bot ke voice channel
        voice_client = await channel.connect()
        await ctx.send(f"🤖 Bot connected to voice channel **{voice_channel_name}**. Start recording for a maximum of 5 minutes...")

        # Reset buffer dan set status rekaman
        recording_data = []
        is_recording = True

        def callback(data):
            if is_recording:
                recording_data.append(data)

        # Mulai mendengarkan audio
        voice_client.listen(discord.AudioSink(callback=callback))

        # Tunggu hingga durasi maksimal atau perintah berhenti
        await asyncio.sleep(MAX_RECORD_DURATION)
        if is_recording:  # Jika rekaman masih aktif setelah durasi
            await stop_recording(ctx)

    except Exception as e:
        await ctx.send(f"Something error: {e}")
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()

# Command: Stop Rekaman Voice Channel
@bot.command()
async def stop_voice(ctx, category_name: str, *, voice_channel_name: str):
    guild = ctx.guild
    
    # Format nama kategori dan channel
    formatted_category_name = category_name.strip()
    formatted_voice_channel_name = voice_channel_name.lower().replace(" ", "-")

    # Temukan kategori berdasarkan nama
    category = discord.utils.get(guild.categories, name=formatted_category_name)
    if not category:
        await ctx.send(f"❌ Category with named **{formatted_category_name}** not found!")
        return

    # Tentukan nama channel default
    default_channel_name = f"{formatted_category_name.lower().replace(' ', '-')}-projects"

    # Temukan channel default dalam kategori
    default_channel = discord.utils.get(category.text_channels, name=default_channel_name)

    # Validasi: Perintah hanya dijalankan di channel default
    if ctx.channel != default_channel:
        await ctx.send(f"❌ This command can only be run on the default channel **{default_channel_name}**!")
        return
    
    # Cek apakah channel sudah ada dalam kategori
    existing_channel = discord.utils.get(category.channels, name=formatted_voice_channel_name)
    if existing_channel:
        await ctx.send(f"✅ Channel with named **{formatted_voice_channel_name}** is already in Category Named **{category.name}**!")
        return
    
    global is_recording
    if not is_recording:
        await ctx.send("❌ No recording in progress!.")
        return

    # Hentikan rekaman
    await stop_recording(ctx)

async def stop_recording(ctx, category_name: str, *, voice_channel_name: str):
    guild = ctx.guild
    
    # Format nama kategori dan channel
    formatted_category_name = category_name.strip()
    formatted_voice_channel_name = voice_channel_name.lower().replace(" ", "-")

    # Temukan kategori berdasarkan nama
    category = discord.utils.get(guild.categories, name=formatted_category_name)
    if not category:
        await ctx.send(f"❌ Category with named **{formatted_category_name}** not found!")
        return

    # Tentukan nama channel default
    default_channel_name = f"{formatted_category_name.lower().replace(' ', '-')}-projects"

    # Temukan channel default dalam kategori
    default_channel = discord.utils.get(category.text_channels, name=default_channel_name)

    # Validasi: Perintah hanya dijalankan di channel default
    if ctx.channel != default_channel:
        await ctx.send(f"❌ This command can only be run on the default channel **{default_channel_name}**!")
        return
    
    # Cek apakah channel sudah ada dalam kategori
    existing_channel = discord.utils.get(category.channels, name=formatted_voice_channel_name)
    if existing_channel:
        await ctx.send(f"✅ Channel with named **{formatted_voice_channel_name}** is already in Category Named **{category.name}**!")
        return
    
    global is_recording, recording_data, voice_client

    is_recording = False  # Ubah status rekaman
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()  # Bot keluar dari voice channel
        voice_client = None

    # Simpan data audio ke file WAV
    wav_filename = "voice_record.wav"
    save_audio(recording_data, wav_filename)

    # Konversi WAV ke MP3 menggunakan FFmpeg
    mp3_filename = "voice_record.mp3"
    convert_to_mp3(wav_filename, mp3_filename)

    # Hapus file WAV setelah konversi
    os.remove(wav_filename)

    # Unggah ke GoFile
    file_url = upload_to_gofiles(mp3_filename)

    await ctx.send(f"✅ Recording completed. File uploaded to GoFile: {file_url}")

# Fungsi: Simpan data audio ke file WAV
def save_audio(data, filename):
    with wave.open(filename, "wb") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit audio
        wav_file.setframerate(48000)  # Frekuensi sampling
        wav_file.writeframes(b"".join(data))

# Fungsi: Konversi WAV ke MP3
def convert_to_mp3(wav_filename, mp3_filename):
    command = ["ffmpeg", "-y", "-i", wav_filename, "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", mp3_filename]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Fungsi: Upload file ke GoFiles
def upload_to_gofiles(filename):
    try:
        with open(filename, "rb") as f:
            response = requests.post("https://store1.gofile.io/uploadFile", files={"file": f}, verify=True)
            if response.status_code != 200:
                return f"Failed to upload. HTTP Status Code: {response.status_code}"
            
            data = response.json()
            if data["status"] == "ok":
                return data["data"]["downloadPage"]
            else:
                return f"Failed to upload file: {data.get('error', {}).get('message', 'Unknown error')}"
    except FileNotFoundError:
        return f"File `{filename}` not found!"
    except Exception as e:
        return f"An error occurred: {e}"
        
@bot.command()
async def end_gp(ctx, *, category_name: str):
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        await ctx.send(f"❌ Category with named **{category_name}** not found!")
        return

    try:
        for channel in category.channels:
            await channel.delete()
        await category.delete()
        await ctx.send(f"✅ Category **{category_name}** successfully deleted along with all channels in it!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to delete categories or channels!")
    except discord.HTTPException as e:
        await ctx.send(f"Something error: {e}")
        
@bot.command()
async def get_email(ctx, user_id: int = None):
    try:
        download_database()
        with app.app_context():
            if user_id is not None:
                # Query satu anggota berdasarkan user_id
                member = Member.query.filter_by(user_id=user_id).first()
                
                emails = [f"Name: {member.name}, Email: {member.email}"]
                email_message = "\n".join(emails)
                
                if member and member.email:
                    await ctx.send(
                        f"📧 Email Member:\n```\n{email_message}\n```"
                    )
                else:
                    await ctx.send(f"❌ No members found with user_id `{user_id}` or email has not been set up.")
            else:
                # Query semua anggota dengan email yang valid
                members = Member.query.filter(Member.email.isnot(None)).all()
                
                emails = [f"Name: {member.name}, Email: {member.email}" for member in members]
                email_message = "\n".join(emails)
                
                if not members:
                    await ctx.send("❌ No email data found in the database!")
                    return
                # Kirim daftar email sebagai pesan
                await ctx.send(f"📧 Here are all the emails found:\n```\n{email_message}\n```")
    except Exception as e:
        await ctx.send(f"❌ An error occurred while retrieving email data: {str(e)}")

        
@bot.command()
@commands.has_role("Admin")  # Hanya admin yang bisa menggunakan perintah ini
async def email_invite(ctx, channel_name: str, user_id: int = None):
    await ctx.send(f"Starting to send invite links for channel `{channel_name}`...")

    try:
        download_database()
        # Cari channel berdasarkan nama
        guild = ctx.guild
        channel = discord.utils.get(guild.channels, name=channel_name)
        if not channel:
            await ctx.send(f"❌ Channel with name `{channel_name}` not found!")
            return

        # Buat link ke channel
        invite = await channel.create_invite(max_age=3600, max_uses=10, unique=True)
        invite_link = invite.url

        # Load template HTML
        template_path = "D:/PYTHON/Project/Gizmo-Notes/webb/templates/email.html"
        with open(template_path, "r", encoding="utf-8") as file:
            html_template = file.read()

        # Query berdasarkan user_id jika diberikan, jika tidak ambil semua anggota
        with app.app_context():
            if user_id is not None:
                member = Member.query.filter_by(user_id=user_id).first()
                if not member or not member.email:
                    await ctx.send(f"❌ No user found with user_id `{user_id}` or email is not set.")
                    return
                members = [member]  # Bungkus dalam list untuk pemrosesan seragam
            else:
                members = Member.query.filter(Member.email.isnot(None)).all()
                if not members:
                    await ctx.send("❌ No email data found in the database!")
                    return

        # Kirim email ke semua anggota
        success_count = 0
        failed_emails = []

        for member in members:
            try:
                # Replace placeholders in template
                personalized_html = html_template.replace("{{name}}", member.name).replace("{{invite_link}}", invite_link)

                # Create email message
                msg = MIMEMultipart("alternative")
                msg["From"] = sender_email
                msg["To"] = member.email
                msg["Subject"] = f"Discord Channel Invite: {channel_name}"
                msg.attach(MIMEText(personalized_html, "html"))

                # Send email
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, member.email, msg.as_string())
                    success_count += 1
                    await ctx.send(f"✅ Sent invite to: {member.email}")

            except Exception as e:
                failed_emails.append(member.email)
                await ctx.send(f"❌ Failed to send to {member.email}: {str(e)}")

        # Send summary
        total_members = len(members)
        await ctx.send(
            f"\n📊 Summary:\n"
            f"Total members: {total_members}\n"
            f"Successfully sent: {success_count}\n"
            f"Failed: {len(failed_emails)}\n"
            f"Failed emails: {', '.join(failed_emails) if failed_emails else 'None'}"
        )

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    download_database()
    bot.run(BOT_TOKEN)