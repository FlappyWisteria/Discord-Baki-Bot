import random

import discord
from discord.ext import commands
from discord import channel
import youtube_dl
import asyncio



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
    "復ッ活ッ",
    "w",
    "このタヌキが...."
    ]

# DiscordToken
TOKEN = "TOKEN"

bot = commands.Bot(
    command_prefix="!",
    case_insensitive=True,
    activity=discord.Game("大擂台賽")
    )

@bot.command()
async def baki(ctx):
    await ctx.send(str(random.choice(l)))

@bot.command()
async def happy(ctx):
    await ctx.send(str("誕生日は終わったよ !bakiで烈海王がしゃべるよ"))

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def play(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('再生中: {}'.format(player.title))

    @commands.command(aliases=["bye","disconnect"])
    async def stop(self, ctx):
        channel = ctx.author.voice.channel
        if channel is None:
            return await ctx.send(VCに接続していません)

        await ctx.voice_client.disconnect()
        await ctx.send("VCから離脱しました。")

    @play.before_invoke

    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("ボイスチャンネルに接続してないよ")
                raise commands.CommandError("ボイスチャンネルに接続してないよ")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


bot.add_cog(Music(bot))

bot.run(TOKEN)
