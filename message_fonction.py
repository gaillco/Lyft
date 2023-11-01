import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = True
intents.message_content = True
intents.members = True
intents.guilds = True


bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
bot_enabled = True 

send_message_enabled = True

# Message in channel discord
@bot.command()
async def send_message_fonction(ctx, channel_id, repeat_count: int, *, message):
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        global send_message_enabled
        if send_message_enabled:
            channel = bot.get_channel(int(channel_id))
            if channel:
                for _ in range(repeat_count):
                    await channel.send(message)
            else:
                await ctx.send("Invalid channel ID")
        else:
            await ctx.send("The send_message command is currently disabled.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Message for user
@bot.command()
async def send_pmessage_fonction(ctx, user_id, repeat_count: int, *, message):
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐", "🫂 || Fan Dream Team", "🛡️ || AER"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        global send_message_enabled
        if send_message_enabled:
            user = await bot.fetch_user(user_id)
        if user:
            for _ in range(repeat_count):
                await user.send(message)
            await ctx.send(f"{repeat_count} messages sent to {user.mention}.")
        else:
            await ctx.send("Invalid user ID.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Clear message
@bot.command()
async def clear_fonction(ctx, amount: int):
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        if amount <= 0:
            await ctx.send("Please specify a valid number of messages to delete.")
            return

        await ctx.channel.purge(limit=amount + 1)

        await ctx.send(f"{amount} messages have been deleted.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Clear all messages
@bot.command()
async def all_fonction(ctx):
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        await ctx.channel.purge()
        await ctx.send("All messages have been deleted.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Disable messages
@bot.command()
async def stop_send_fonction(ctx):
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        global send_message_enabled
        send_message_enabled = False
        await ctx.send("The send_message command has been disabled.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Enabled messages
@bot.command()
async def start_send_fonction(ctx):
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        global send_message_enabled
        send_message_enabled = True
        await ctx.send("The send_message command has been enabled.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Delete channel
@bot.command()
async def delc_fonction(ctx):
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        try:
            await ctx.channel.delete()
        except discord.Forbidden:
            await ctx.send("Je n'ai pas la permission de supprimer ce canal.")
        except discord.HTTPException:
            await ctx.send("Une erreur s'est produite lors de la suppression du canal.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Handle command errors
@send_message_fonction.error
async def send_message_error(ctx, error):
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Invalid command format. Use: !send_message <channel_id> <repeat_count> <message>")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Make sure to use valid channel_id and repeat_count values.")
        else:
            await ctx.send("Sorry, you do not have permission to use this command.")

