import discord
from discord.ext import commands
import logging
import os
import json
import base64
import requests
from keep_alive import keep_alive


keep_alive() 


# helper functions
def get_token():
    token_path = os.path.join(os.path.dirname(__file__), "token.json")
    with open(token_path, 'r') as token_file:
        token = json.load(token_file)['token']

    unpad_token = str(token).replace("====", "")
    final_token = base64.b64decode(unpad_token).decode()

    return final_token


intents = discord.Intents.default()
intents.message_content = True
intents.members = True



bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)


@bot.command()
async def like(ctx, *, uid):
    try:
        response = requests.get(f"https://nhk-likes-bot.vercel.app/like?uid={uid}&server=SG")
        
        if response.status_code != 200:
            await ctx.send(f"❌ API returned status code {response.status_code}")
            return
        
        try:
            data = response.json()
        except ValueError:
            await ctx.send(f"❌ API did not return valid JSON:\n{response.text}")
            return
        
        status = data.get('likes_added', 0)

        if status == 0:
            embed = discord.Embed(
                title="Transaction Failed ❌",
                description="You have already claimed todays likes 😔. Please try again tommorrow ❤️‍🔥",
                color=discord.Color.red()
            )
            await ctx.send(f'{ctx.author.mention}', embed=embed)
        else:
            embed = discord.Embed(
                title=f"Player: {data.get('player', 'Unknown')}",
                description=(
                    f"UID: {data.get('uid', 'Unknown')}\n"
                    f"Likes Added: {data.get('likes_added', 0)}\n"
                    f"Likes Before: {data.get('likes_before', 0)}\n"
                    f"Likes After: {data.get('likes_after', 0)}\n"
                    f"Credits: {data.get('credits', 'Nighthawks')}"
                ),
                color=discord.Color.blue()
            )

            await ctx.send(f'{ctx.author.mention} - Success ✅✅', embed=embed)

    except Exception as e:
        await ctx.send(f"Error fetching likes: {e}")

if __name__ == "__main__":
    bot.run(token=get_token())