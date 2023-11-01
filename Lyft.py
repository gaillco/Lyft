import discord
import json
from discord.ext import commands

from help_fonction import help_staff
from help_fonction import help_user
from help_fonction import help_ticket_fonction
from ticket_fonction import setup_ticket_fonction
from ticket_fonction import bot
from message_fonction import send_message_fonction
from message_fonction import send_pmessage_fonction
from message_fonction import delc_fonction
from message_fonction import clear_fonction
from message_fonction import all_fonction
from message_fonction import stop_send_fonction
from message_fonction import start_send_fonction
from message_test import createticket

intents = discord.Intents.default()
intents.typing = True
intents.message_content = True
intents.members = True
intents.guilds = True

ticket_counter = 1

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
bot_enabled = True 

send_message_enabled = True

ticket_category_name = "Tickets"

SUPPORT_CHANNEL_ID = 1168994911153029130
server_id = 1159020670575968371
bot_token = 'MTE2ODQ4MTA4MDY4OTU2OTgxMg.GFavhS.shT-7dgxpjvvAInMB1vaa8Jsq7K7KIpx2h-X_I'

# Message active on console
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'With the id {bot.user.id}')
    for guild in bot.guilds:
        print(f"Bot is active on the server {guild.name} (ID: {guild.id})\n     Owned by {guild.owner.display_name} (ID : {guild.owner.id})")
    owner = await bot.application_info()
    owner_user = owner.owner

    # Message active on Discord 
    for guild in bot.guilds:
        await owner_user.send(f"Bot is now active on the server {guild.name} (ID: {guild.id})\n     Owned by {guild.owner.display_name} (ID : {guild.owner.id}).")

@bot.event
async def on_disconnect():
    owner = await bot.application_info()
    owner_user = owner.owner

    for guild in bot.guilds:
        await owner_user.send(f"Bot is now offline on the server {guild.name} (ID: {guild.id}).")

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
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        global bot_enabled
        bot_enabled = not bot_enabled
        status = "activated" if bot_enabled else "disabled"
        await ctx.send(f"The bot is now {status}.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")


# Check who is the owner
@bot.command()
async def is_owner(ctx):
    allowed_roles = ["🫂 || Fan Dream Team", "🛡️ || AER", "GOAT 🐐","👑  || Owner", "<@root>"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        guild = ctx.guild
        author = ctx.author

        if guild and guild.owner == author:
            await ctx.send(f'{author.display_name} is the owner of this server!')
        else:
            await ctx.send(f'{author.display_name} is not the owner of this server. The owner is {guild.owner.display_name} (ID : {guild.owner.id}).')
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")


# List of available orders for user
@bot.command()
async def help(ctx):
    result = await help_user(ctx)
    if result:
        await ctx.send(result)
    else:
        ctx.send("The command help has been run by 'name'")


# List of available orders for staff
@bot.command()
async def help_all(ctx):
    result = await help_staff(ctx)
    if result:
        await ctx.send(result)
    else:
        ctx.send(f"The command help_all has been run by 'name'")

# List of available orders for ticket
@bot.command()
async def help_ticket(ctx):
    result = await help_ticket_fonction(ctx)
    if result:
        await ctx.send(result)
    else:
        ctx.send("The command help_ticket has been run by 'name'")

# Message in chanel discord
@bot.command()
async def send_message(ctx):
    result = await send_message_fonction(ctx)
    if result:
        await ctx.send(result)
    else:
        ctx.send("The command send_message has been run by 'name'")
    
# Message for user
@bot.command()
async def send_pmessage(ctx):
    result = await send_pmessage_fonction(ctx)
    if result:
        await ctx.send(result)
    else:
        ctx.send("The command send_pmessage has been run by 'name'")

# Delete channel
@bot.command()
async def delc(ctx):
    result = await delc_fonction(ctx)
    if result:
        await ctx.send(result)
    else:
        ctx.send("The command delc has been run by 'name'")

# Clear messages
@bot.command()
async def clear(ctx):
    result =  await clear_fonction(ctx)
    if result:
        await ctx.send(result)
    else:
        ctx.send("The command clear has been run by 'name'")

# Clear all messages
@bot.command()
async def all(ctx):
    result = await all_fonction(ctx)
    if result:
        await ctx.send(result)
    else:
        ctx.send("The command all has been run by 'name'")

# Disable messages
@bot.command()
async def stop_send(ctx):
    result = await stop_send_fonction(ctx)
    if result:
        await ctx.send(result)
    else:
        ctx.send("The command stop_send has been run by 'name'")

# Enabled messages
@bot.command()
async def start_send(ctx):
    result = start_send_fonction(ctx)
    if result:
        await ctx.send(result)
    else:
        ctx.send("The command start_send has been run by 'name'")

# Ticket system
@bot.command()
async def setup_ticket(ctx):
    result = await setup_ticket_fonction(ctx)
    if result:
        await ctx.send(result)
    else:
        await ctx.send("Your ticket has been created.")

@bot.command()
async def setup_ticket_2(ctx):
    result = await createticket(ctx)
    if result:
        await ctx.send(result)
    else:
        ctx.send("The command help has been run by 'name'")

@bot.event
async def on_raw_reaction_add(ctx):
    # Récupère le serveur (guild) et le membre (user) correspondant au ctx
    guild = bot.get_guild(ctx.guild_id)
    member = guild.get_member(ctx.user_id)

    if member == bot.user:
        return  # Ignore les réactions du bot lui-même

    if ctx.channel_id == SUPPORT_CHANNEL_ID:
        # Crée un nouveau salon texte pour le ticket
        ticket_category = discord.utils.get(guild.categories, name="Tickets")
        if not ticket_category:
            ticket_category = await guild.create_category("Tickets")

        ticket_channel = await ticket_category.create_text_channel(f'ticket-{member.display_name}')
        await ticket_channel.send(embed=create_ticket_embed())

        # Répond dans le canal de support
        support_channel = guild.get_channel(SUPPORT_CHANNEL_ID)
        if support_channel:
            await support_channel.send(f"Ticket créé dans {ticket_channel.mention}")

def create_ticket_embed():
    embed = discord.Embed(color=discord.Color.green(), description=f"""\n
            Your ticket channel has been created!\n
            React with ❌ to close this ticket\n
            React with 🔒 to lock this ticket\n
            """)
    embed.set_footer(text=bot.user.name, icon_url=bot.user.avatar)
    return embed

# Run the bot
bot.run(bot_token) 