import random

import discord
from discord import channel
from discord.ext import commands

# 烈海王セリフlist
l = [
    "私は一向にかまわんッッ",
    "ウワアアアオオオオ",
    "キサマ等の居る場所は既に——我々が2000年前に通過した場所だッッッ",
    "海王のレベルも堕ちたものだ……",
    "わたしが餌となっては如何かッ",
    "こここそが……ッッ、消力本番！！！",
    "グローブを外したのだよ",
    "問題はない！！　15メートルまでなら！！！",
    "喰うんだ",
    "強さとはおのれの意を貫き通す力、我がままを押し通す力・・・とするならば敗北を熱望しながら現時点まで無敗のあなたは・・・一度も勝ったことがない",
    "このまま無事帰れると思ってるのか",
    "一つ教えといてやろう　君らのいる場所は我々はすでに三千年以上前に通過している",
    "いつの時も どんな時も 金的は絶対です",
    "百戦錬磨の愚地氏は闘いが安易ではないことなど知りつくしているのだ　闘いとは不都合なもの、闘いとは思い通りにならないもの・・・　武神愚地独歩にとってそれが闘いなのだ！",
    "成る程オオオオッッ",
    "まだ１分には数秒残してる…………　どうだ　まだ継続けるか",
    "「黄河は水たまりを叱りはしない」という　ことわざがあるが私の考えは違う",
    "自己の意を貫き通す力　我儘を押し通す力　私にとって強さとはそういうものです",
    "復ッ活ッ"
    ]

# DiscordToken
TOKEN = "ODU0OTk2NTgzNzQwMzQyMzEz.YMsDng.quevtXKLwfFzYwvtqggvfLAS57U"

client = discord.Client()

# bot = commands.Bot(command_prefix="")

# プレイ中のゲームを表示
presence = discord.Game("大擂台賽")

@client.event
async def on_ready():
    print("bot起動!")
    await client.change_presence(activity=presence)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == "!baki":
        await message.channel.send(str(random.choice(l)))
    if message.content == "!happy":
        await message.channel.send(str("誕生日は終わったよ !bakiで烈海王がしゃべるよ"))

client.run(TOKEN)
