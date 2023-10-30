import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = True
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)  # Provide the 'intents' parameter

send_message_enabled = True

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def send_message(ctx, channel_id, *, message):
    global send_message_enabled
    if send_message_enabled:
        channel = bot.get_channel(int(channel_id))
        if channel:
            await channel.send(message)
        else:
            await ctx.send("Invalid channel ID")
    else:
        await ctx.send("The send_message command is currently disabled.")

@bot.command()
async def stop_send(ctx):
    global send_message_enabled
    send_message_enabled = False
    await ctx.send("The send_message command has been disabled.")

@bot.command()
async def start_send(ctx):
    global send_message_enabled
    send_message_enabled = True
    await ctx.send("The send_message command has been enabled.")

# Run the bot
bot.run('MTE2ODQ4MTA4MDY4OTU2OTgxMg.GBvpYY._dTFXTlyqf6r6_z8L8eYTwu7tpmjlrCyEtuOFg')
