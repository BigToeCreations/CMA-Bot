import os
import requests
import discord
from discord.ext import tasks

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def format_number(n):
    if n >= 1000000:
        return f"{n / 1000000:.2f}M"
    if n >= 1000:
        return f"{n / 1000:.2f}K"
    return str(n)

# 👇 ADD YOUR CHANNELS HERE
CHANNELS = [
    {
        "yt_id": "UCJhc-jDzk8S21jDwEzzKUEQ",
        "discord_id": 1483873954451030077
    },
    {
        "yt_id": "UCa0l1zX4lqrP1l-CrZoPeZQ",
        "discord_id": 1483874805639024670
    }
]

def get_youtube_data(channel_id):
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "statistics,snippet",
        "id": channel_id,
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
        for ch in CHANNELS:
            name, subs = get_youtube_data(ch["yt_id"])
            channel = client.get_channel(ch["discord_id"])

            if channel:
                await channel.edit(name=f"{name}: {format_number(subs)}")

        print("Updated all channels!")

    except Exception as e:
        print("Error:", e)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    update_stats.start()

client.run(DISCORD_TOKEN)