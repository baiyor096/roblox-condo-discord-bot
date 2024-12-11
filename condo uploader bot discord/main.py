import os
import json
from discord import Webhook, RequestsWebhookAdapter, Embed
from discord.ext import commands
import aiohttp
import asyncio

bot = commands.Bot(command_prefix="-")  # กำหนด prefix สำหรับคำสั่ง

# โหลดตัวแปรจาก environment
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Streaming(name='-Upload', url='https://www.twitch.tv/'))

async def get_xcsrf_token(cookie):
    async with aiohttp.ClientSession(cookies={'.ROBLOSECURITY': cookie}) as session:
        async with session.post("https://auth.roblox.com/v2/logout") as response:
            if response.status == 403:
                return response.headers['x-csrf-token']
    return None

async def fetch_user_data(cookie, token):
    async with aiohttp.ClientSession(cookies={'.ROBLOSECURITY': cookie}) as session:
        async with session.get(
            "https://users.roblox.com/v1/users/authenticated",
            headers={'x-csrf-token': token}
        ) as response:
            return await response.json()

async def upload_game(cookie, token, game_file_path):
    async with aiohttp.ClientSession(cookies={'.ROBLOSECURITY': cookie}) as session:
        # ดึงข้อมูล userId และ gameId
        user_data = await fetch_user_data(cookie, token)
        user_id = user_data.get("id")
        if not user_id:
            print("ไม่สามารถดึงข้อมูล user_id ได้")
            return None

        # อัปโหลดไฟล์เกม
        with open(game_file_path, "rb") as file:
            async with session.post(
                "https://data.roblox.com/Data/Upload.ashx",
                headers={'x-csrf-token': token, 'Content-Type': 'application/xml'},
                data=file
            ) as upload_response:
                if upload_response.status == 200:
                    return user_id
    return None

async def notify_discord(game_id):
    webhook = Webhook.from_url(WEBHOOK_URL, adapter=RequestsWebhookAdapter())
    embed = Embed(
        title="เกมใหม่ถูกอัปโหลด!",
        description=f"[คลิกที่นี่เพื่อเล่น!](https://www.roblox.com/games/{game_id}/)",
        color=0x00ff00
    )
    embed.set_footer(text="สร้างโดย Async")
    webhook.send(embed=embed)

@bot.command()
async def Upload(ctx):
    await ctx.send("กรุณาใส่คุกกี้ .ROBLOSECURITY:")
    try:
        cookie_message = await bot.wait_for('message', timeout=60.0)
        cookie = cookie_message.content.strip()

        if '_|WARNING' not in cookie:
            await ctx.send(":x: คุกกี้ไม่ถูกต้อง!")
            return

        # ดึง X-CSRF Token
        token = await get_xcsrf_token(cookie)
        if not token:
            await ctx.send(":x: ไม่สามารถดึง X-CSRF Token ได้!")
            return

        # อัปโหลดเกม
        game_file_path = "file.rbxlx"  # เปลี่ยน path ตามไฟล์จริง
        user_id = await upload_game(cookie, token, game_file_path)

        if user_id:
            await ctx.send(":white_check_mark: อัปโหลดสำเร็จ!")
            await notify_discord(user_id)
        else:
            await ctx.send(":x: การอัปโหลดล้มเหลว!")
    except asyncio.TimeoutError:
        await ctx.send(":x: การใส่คุกกี้เกินเวลาที่กำหนด!")

# รันบอท
if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
else:
    print("กรุณาตั้งค่า DISCORD_TOKEN ใน environment variables")
