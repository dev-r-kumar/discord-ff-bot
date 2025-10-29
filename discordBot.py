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
@commands.has_role("admin") #only admins to generate license key  !
async def licensekey(ctx):
    try:
        response = requests.get(f"https://nhkxcheat.pythonanywhere.com/api/auth/generate-license?type=week&quantity=1")
        
        if response.status_code != 200:
            await ctx.send(f"❌ API returned status code {response.status_code}")
            return
        
        try:
            data = response.json()
        except ValueError:
            await ctx.send(f"❌ API did not return valid JSON:\n{response.text}")
            return
        

        key = list(data['generated_keys'][0].keys())[0]

   
        embed = discord.Embed(
            title="License Key Bot",
            description=f"1 week license key.\nLicense Key: **{key}**",
            color=discord.Color.red()
        )
        await ctx.send(f'{ctx.author.mention}', embed=embed)


    except Exception as e:
        await ctx.send(f"{e}")


@bot.command()
@commands.has_role("admin")
async def refresh(ctx):
    try:
        response = requests.get(f"https://ff-like-api-two.vercel.app/refresh-tokens")

        if response.status_code != 200:
            await ctx.send(f"❌ API returned status code {response.status_code}")
            return
        

        try:
            data = response.json()
        except ValueError:
            await ctx.send(f"❌ API did not return valid JSON:\n{response.text}")
            return
        

        embed = discord.Embed(
            title="Info",
            description=f"Status: {data.get('status', 'Unable to refresh tokens ❌')}",
            color=discord.Color.blue()
        )

        await ctx.send(f'{ctx.author.mention}', embed = embed)

    except Exception as e:
        await ctx.send(f"Error fetching likes: {e}")


if __name__ == "__main__":
    bot.run(token=get_token())

