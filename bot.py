import discord
import os
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import date

DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

def make_msg():
    today = date.today()
    today_str = str(today.year) + "년 " + str(today.month) + "월 " \
        + str(today.day) + "일"
    next_str = str(today.year) + "년 " + str(today.month) + "월 " \
        + str(today.day) + "일"

    msg = today_str +" Daily Scrum 입니다.\n" \
        + "작성 기한 : "+ today_str + " 22:00:00 ~ " + next_str + " 10:00:00\n"\
        "1. 오늘 내가 완수한 일\n" \
        + "2. 내일 내가 해야할 일\n" \
        + "3. 현재 곤란하고 어려운 일\n" \
        + "에 대해 이야기 해 봅시다 🙂"
    
    return msg

@bot.event
async def on_ready():    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_message, CronTrigger(hour="13", minute="00"))
    scheduler.start()

async def send_message():
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    await channel.send(make_msg())

bot.run(DISCORD_BOT_TOKEN)  