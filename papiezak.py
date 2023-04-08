import discord
import asyncio
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

client = discord.Client(intents=discord.Intents.all())


async def play_sound(voice_client):
    try:
        source = await discord.FFmpegOpusAudio.from_probe('barka.mp3')

        print(f"Audio file loaded: {source}")
        voice_client.play(source)
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await asyncio.sleep(source.duration)
        await voice_client.disconnect()
        voice_client.cleanup()
    except Exception as e:
        print(f"Audio could not be played: {e}")


@client.event
async def on_ready():
    print('Bot is ready')
    now = datetime.datetime.now()

    target_time = datetime.time(hour=21, minute=37)
    if now.time() >= target_time:
        print(f"Current time: {now.time()}. Bot did not join channel.")
        return
    else:
        print(f"Current time: {now.time()}. Bot has joined at {target_time}.")
        await asyncio.sleep((datetime.datetime.combine(datetime.date.today(), target_time) - now).total_seconds())
        channel = client.get_channel(int(CHANNEL_ID))
        if channel is not None:
            try:
                voice_client = await channel.connect()
                print(f'{client.user} joined voice chat.')
                await asyncio.sleep(1)
                await play_sound(voice_client)
                await voice_client.disconnect()
                print(f'{client.user} left voice chat.')
            except Exception as e:

                print(f"Error during joining channel : {e}")
        else:
            print(f"Did not find a channel of ID {CHANNEL_ID}.")

client.run(TOKEN)
