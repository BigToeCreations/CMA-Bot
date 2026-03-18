import os
import requests
import discord
from discord.ext import tasks

# ===== PASTE YOUR STUFF HERE =====
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
SUB_CHANNEL_ID = int(os.getenv("SUB_CHANNEL_ID"))
# =================================

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def format_number(n):
    if n >= 1000000:
        return f"{n / 1000000:.2f}M"
    if n >= 1000:
        return f"{n / 1000:.2f}K"
    return str(n)

def get_youtube_subs():
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "statistics,snippet",
        "id": YOUTUBE_CHANNEL_ID,
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    item = data["items"][0]
    name = item["snippet"]["title"]
    subs = int(item["statistics"]["subscriberCount"])

    return name, subs

@tasks.loop(minutes=10)
async def update_stats():
    try:
        name, subs = get_youtube_subs()

        channel = client.get_channel(SUB_CHANNEL_ID)

        if channel:
            await channel.edit(name=f"{name}: {format_number(subs)}")

        print("Updated!")

    except Exception as e:
        print("Error:", e)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    update_stats.start()

client.run(DISCORD_TOKEN)
