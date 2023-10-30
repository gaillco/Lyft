import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

bot_enabled = True 

send_message_enabled = True

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'With the id {bot.user.id}')

# List of available orders for user
@bot.command()
async def help(ctx):
    allowed_roles = ["👤 || Epitechien(ne)", "GOAT 🐐", "@root"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        embed = discord.Embed(title='__List of available orders :__\n', color=discord.Color.blue(), description="""
                        **!help** : Displays this list of commands\n
                        **!send_pmessage** : Sends messages to a user on the discord server, command to be followed : ```!send_pmessage <user_id> <repeat_count> <message>```\n""",
                        )
        roles = [role.name for role in ctx.author.roles]
        roles_text = ', '.join(roles)
        
        footer_text = "Don't forget to remove the ''< >'' in the commands"
        
        if ctx.author.avatar is not None:
            embed.set_footer(text=f"{ctx.author.name} - {footer_text} - [{roles_text}]", icon_url=ctx.author.avatar.url)
        else:
            embed.set_footer(text=f"{ctx.author.name} - {footer_text} - [{roles_text}]")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

    await ctx.send(embed=embed)

# List of available orders for staff
@bot.command()
async def help_all(ctx):
    allowed_roles = ["@root", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        embed = discord.Embed(title='__List of available orders :__\n', color=discord.Color.blue(), description="""
                        **!help** : Displays this list of commands\n
                        **!toggle**: Activate or desactivate the bot\n
                        **!all** : Delete all messages in the chanel discord\n
                        **!stop_send** : Disable message sending to chanel discord\n
                        **!start_send** : Enable message sending to chanel discord\n
                        **!send_message** : Send messages in a discord chanel, command to be followed : ```!send_message <channel_id> <repeat_count> <message>```\n
                        **!send_pmessage** : Sends messages to a user on the discord server, command to be followed : ```!send_pmessage <user_id> <repeat_count> <message>```\n
                        **!clear** : Delete messages in a chanel discord, command to be followed : ```!clear <amount>```\n""",
                        )
        roles = [role.name for role in ctx.author.roles]
        roles_text = ', '.join(roles)

        footer_text = "Don't forget to remove the ''< >'' in the commands"

        if ctx.author.avatar is not None:
            embed.set_footer(text=f"{ctx.author.name} - {footer_text} - [{roles_text}]", icon_url=ctx.author.avatar.url)
        else:
            embed.set_footer(text=f"{ctx.author.name} - {footer_text} - [{roles_text}]")

    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

    await ctx.send(embed=embed)

# Check bot activation
@bot.event
async def on_message(message):
    if bot_enabled == True:
        await bot.process_commands(message)
    elif bot_enabled == False and message.content == "!toggle":
        await bot.process_commands(message)

# Bot activation
@bot.command()
async def toggle(ctx):
    allowed_roles = ["@root", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        global bot_enabled
        bot_enabled = not bot_enabled
        status = "activated" if bot_enabled else "disabled"
        await ctx.send(f"The bot is now {status}.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Message in chanel discord
@bot.command()
async def send_message(ctx, channel_id, repeat_count: int, *, message):
    allowed_roles = ["@root", "GOAT 🐐"]
    
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
async def send_pmessage(ctx, user_id, repeat_count: int, *, message):
    allowed_roles = ["@root", "GOAT 🐐", "👤 || Epitechien(ne)"]
    
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

# Clear messages
@bot.command()
async def clear(ctx, amount: int):
    allowed_roles = ["@root", "GOAT 🐐"]
    
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
async def all(ctx):
    allowed_roles = ["@root", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        await ctx.channel.purge()
        await ctx.send("All messages have been deleted.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Disable messages
@bot.command()
async def stop_send(ctx):
    allowed_roles = ["@root", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        global send_message_enabled
        send_message_enabled = False
        await ctx.send("The send_message command has been disabled.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Enabled messages
@bot.command()
async def start_send(ctx):
    allowed_roles = ["@root", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        global send_message_enabled
        send_message_enabled = True
        await ctx.send("The send_message command has been enabled.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Handle command errors
@send_message.error
async def send_message_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Invalid command format. Use: !send_message <channel_id> <repeat_count> <message>")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument. Make sure to use valid channel_id and repeat_count values.")

# Run the bot
bot.run('MTE2ODQ4MTA4MDY4OTU2OTgxMg.GBvpYY._dTFXTlyqf6r6_z8L8eYTwu7tpmjlrCyEtuOFg') 
