import discord
from discord.ext import commands, tasks
from datetime import datetime
import requests

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

BASE_API_URL = 'https://muslimsalat.p.rapidapi.com/bandung.json'  # replace with your base API URL
CITY = 'Bandung'
API_URL = f"{BASE_API_URL}?kota={CITY}"

headers = {
    'x-rapidapi-host': "muslimsalat.p.rapidapi.com",  # replace with your RapidAPI host
    'x-rapidapi-key': "fe7ac125c5msh94f9c196609b1eep12fb18jsndc6f9e5920c3",  # replace with your RapidAPI key
}


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    channel = bot.get_channel('your_channel_id')  # replace with your channel id
    check_prayer_time.start(channel)


@tasks.loop(minutes=1.0)
async def check_prayer_time(channel):
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()

        fajr = time_adjust(data['items'][0]['fajr'])
        dhuhr = time_adjust(data['items'][0]['dhuhr'])
        asr = time_adjust(data['items'][0]['asr'])
        maghrib = time_adjust(data['items'][0]['maghrib'])
        isha = time_adjust(data['items'][0]['isha'])

        current_time = get_current_time()

        if current_time == fajr:
            await channel.send(":mosque: It's now **Fajr** prayer time in **Bandung**. Let's pray :pray: ")
        elif current_time == dhuhr:
            await channel.send(":mosque: It's now **Dhuhr** prayer time in **Bandung**. Let's pray :pray: ")
        elif current_time == asr:
            await channel.send(":mosque: It's now **Asr** prayer time in **Bandung**. Let's pray :pray: ")
        elif current_time == maghrib:
            await channel.send(":mosque: It's now **Maghrib** prayer time in **Bandung**. Let's pray :pray:  ")
        elif current_time == isha:
            await channel.send(":mosque: It's now **Isha** prayer time in **Bandung**. Let's pray :pray:  ")


def time_adjust(time_str):
    # Adjust prayer time format to match with current time format
    return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")


def get_current_time():
    # Get current time in same format as prayer times
    return datetime.now().strftime("%H:%M")


bot.run('MTE2NDkyOTY4MzQzMTg4NjkwMA.G9QuC8.2ys_vh0JUnnOA4AyOo3tXYxDAqQSHyYbB6gyJ0')  # replace with your bot token
