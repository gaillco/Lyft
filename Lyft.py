import discord
from discord.ext import commands
from discord.ext.commands import has_any_role
import discord.ui as ui
from discord import app_commands
from discord.ui import Button, View
from tokens import bot_token, SUPPORT_CHANNEL_ID, DESTINATION_CHANNEL_ID, SOURCE_SERVER_ID, DESTINATION_SERVER_ID, DESTINATION_CHANNEL_MAIN_ID, DESTINATION_SERVER_MAIN_ID, DESTINATION_CHANNEL_ID_delete, DESTINATION_CHANNEL_ID_edited, LOG__KICK_CHANNEL_ID

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

@bot.command(name="sync")
async def sync(interaction):
    await bot.tree.sync()
    await interaction.reply("Commands synced !")

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

    if message.author == bot.user:
        return

# Block server invite links
    if any(word in message.content for word in ["discord.gg/", "discord.com/invite/", "discordapp.com/invite/", "discord.me/", "discord.io/", "discord.tk/", "discordlist.net/", "discord.ly/", "discord.link/", "disboard.org/", "discord.gg"]):
            await message.delete()
            await message.channel.send(f"Sorry {message.author.display_name}, sending server invite links is not allowed.")
            await bot.process_commands(message)

# Log send message
    if message.guild is not None and message.guild.id == SOURCE_SERVER_ID:
        if not message.author.bot:
            destination_server = bot.get_guild(DESTINATION_SERVER_ID)
            if destination_server:
                destination_channel = destination_server.get_channel(DESTINATION_CHANNEL_ID)
                if destination_channel:
                    await destination_channel.send(f"{message.author.display_name} : {message.content} in {message.channel.mention}")

# Message in channel discord
    if message.guild is not None and message.guild.id == SOURCE_SERVER_ID:
        if not message.author.bot:
            destination_server = bot.get_guild(DESTINATION_SERVER_MAIN_ID)
            if destination_server:
                destination_channel = destination_server.get_channel(DESTINATION_CHANNEL_MAIN_ID)
                if destination_channel:
                    await destination_channel.send(f"{message.author.display_name} : {message.content} in {message.channel.mention}")


# Log edited messages
@bot.event
async def on_message_edit(before, after):
    if before.guild.id == SOURCE_SERVER_ID:
        log_channel = bot.get_channel(DESTINATION_CHANNEL_ID_edited)
        if log_channel:
            if before.author == bot.user:
                await log_channel.send(f"Message edited by the bot (ID: {before.author.id})")
            else:
                author_name = before.author.display_name if before.author else "Unknown User"
                await log_channel.send(f"Message edited by {author_name}\nID = {before.author.id}\nContent of the message before : '**{before.content}**'\nContent of the message after : '**{after.content}**'\nIn {before.channel.mention}")

# Log deleted messages 
@bot.event
async def on_message_delete(message):
    if message.guild.id == SOURCE_SERVER_ID:
        log_channel = bot.get_channel(DESTINATION_CHANNEL_ID_delete)
        if log_channel:
            if message.author == bot.user:
                await log_channel.send(f"Message deleted by the bot (ID: {message.author.id})")
            else:
                author_name = message.author.display_name if message.author else "Unknown User"
                await log_channel.send(f"Message deleted by {author_name}\nID = {message.author.id}\nContent of the message: '**{message.content}**'\nIn {message.channel.mention}")

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
    allowed_roles = ["🫂 || Fan Dream Team", "🛡️ || AER", "GOAT 🐐", "👑  || Owner", "@root"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        embed = discord.Embed(title='__List of available orders :__\n', color=discord.Color.blue(), description="""
                        **!help** : Displays the user list of commands\n
                        **!help_all** : Displays the staff list of commands\n
                        **!help_ticket** : Displays the action for the ticket\n
                        **!is_owner** : To display who is the owner\n
                        **!send_pmessage** : Sends messages to a user on the discord server, command to be followed : ```!send_pmessage <user_id> <repeat_count> <message>```\n""",
                        )
        roles = [role.name for role in ctx.author.roles]
        roles_text = ', '.join(roles)
        
        footer_text = "                   Don't forget to remove the ''< >'' in the commands\n\n"
        
        if ctx.author.avatar is not None:
            embed.set_footer(text=f"{ctx.author.name}   {footer_text} - [ {roles_text} ] - ", icon_url=ctx.author.avatar.url)
        else:
            embed.set_footer(text=f"{ctx.author.name}   {footer_text} - [ {roles_text} ] - ")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

    await ctx.send(embed=embed)


# List of available orders for staff
@bot.command()
async def help_all(ctx):
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        embed = discord.Embed(title='__List of available orders :__\n', color=discord.Color.blue(), description="""
                        **!help** : Displays the user list of commands\n
                        **!help_all** : Displays the staff list of commands\n
                        **!help_ticket** : Displays the action for the ticket\n
                        **!toggle**: Activate or desactivate the bot\n
                        **!is_owner** : To display who is the owner\n
                        **!all** : Delete all messages in the chanel discord\n
                        **!stop_send** : Disable message sending to chanel discord\n
                        **!start_send** : Enable message sending to chanel discord\n
                        **!delc** : Delete the chanel discord\n
                        **!send_message** : Send messages in a discord chanel, command to be followed : ```!send_message <channel_id> <repeat_count> <message>```\n
                        **!send_pmessage** : Sends messages to a user on the discord server, command to be followed : ```!send_pmessage <user_id> <repeat_count> <message>```\n
                        **!clear** : Delete messages in a chanel discord, command to be followed : ```!clear <amount>```\n
                        """,)
        roles = [role.name for role in ctx.author.roles]
        roles_text = ', '.join(roles)

        footer_text = "                   Don't forget to remove the ''< >'' in the commands\n\n"

        if ctx.author.avatar is not None:
            embed.set_footer(text=f"{ctx.author.name}  {footer_text} - [ {roles_text} ] - ", icon_url=ctx.author.avatar.url)
        else:
            embed.set_footer(text=f"{ctx.author.name}  {footer_text} - [ {roles_text} ] - ")

    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

    await ctx.send(embed=embed)

# List of available orders for ticket
@bot.command()
async def help_ticket(ctx):
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]

    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)

    if has_allowed_role:
        embed = discord.Embed(title='__List of commande for ticket__\n', color=discord.Color.blue(), description="""
                            **!setup_ticket** : Create the setup for ticket\n
                            **🚫** : Only for admin, delete the ticket\n
                            **❌** : Close the ticket\n
                            **🔒** : Lock the ticket\n
                            **🔓** : Unlock the ticket\n
                            """,)
        roles = [role.name for role in ctx.author.roles]
        roles_text = ', '.join(roles)

        if ctx.author.avatar is not None:
            embed.set_footer(text=f"{ctx.author.name} - [ {roles_text} ] - ", icon_url=ctx.author.avatar.url)
        else:
            embed.set_footer(text=f"{ctx.author.name} - [ {roles_text} ] - ")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Message in chanel discord
@bot.command()
async def send_message(ctx, channel_id, repeat_count: int, message):
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
async def send_pmessage(ctx, user_id, repeat_count: int, message):
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

# Delete channel
@bot.command()
async def delc(ctx):
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

# Clear messages
@bot.command()
async def clear(ctx, amount: int):
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
async def all(ctx):
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        await ctx.channel.purge()
        await ctx.send("All messages have been deleted.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Disable messages
@bot.command()
async def stop_send(ctx):
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
async def start_send(ctx):
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        global send_message_enabled
        send_message_enabled = True
        await ctx.send("The send_message command has been enabled.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Create ticket
@bot.command()
async def setup_ticket(ctx):
    guild = ctx.guild

    if ctx.channel.id == SUPPORT_CHANNEL_ID:
        owner_button = Button(label="Owner", style=discord.ButtonStyle.green, emoji="👑")

        async def owner_button_callback(interaction):
            member = interaction.user
            ticket_category = discord.utils.get(guild.categories, name="Tickets")
            if not ticket_category:
                ticket_category = await guild.create_category("Tickets")
            
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(view_channel=True)
            }
            
            ticket_channel = await ticket_category.create_text_channel(f'ticket-{member}', overwrites=overwrites)

            await interaction.response.send_message(f"Ticket created in {ticket_channel.mention}", ephemeral=True)

        owner_button.callback = owner_button_callback

    if ctx.channel.id == SUPPORT_CHANNEL_ID:
        fans_dream_team_button = Button(label="Fan Dream Team's", style=discord.ButtonStyle.green, emoji="🫂")

        async def fans_dream_team_button_callback(interaction):
            member = interaction.user
            ticket_category = discord.utils.get(guild.categories, name="Tickets")
            if not ticket_category:
                ticket_category = await guild.create_category("Tickets")
            
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(view_channel=True)
            }
            
            ticket_channel = await ticket_category.create_text_channel(f'ticket-{member}', overwrites=overwrites)

            await interaction.response.send_message(f"Ticket created in {ticket_channel.mention}", ephemeral=True)

        fans_dream_team_button.callback = fans_dream_team_button_callback
        
    if ctx.channel.id == SUPPORT_CHANNEL_ID:
        aer_button = Button(label="AER", style=discord.ButtonStyle.green, emoji="🛡️")

        async def aer_button_callback(interaction):
            member = interaction.user
            ticket_category = discord.utils.get(guild.categories, name="Tickets")
            if not ticket_category:
                ticket_category = await guild.create_category("Tickets")
            
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(view_channel=True)
            }
            
            ticket_channel = await ticket_category.create_text_channel(f'ticket-{member}', overwrites=overwrites)

            await interaction.response.send_message(f"Ticket created in {ticket_channel.mention}", ephemeral=True)

        aer_button.callback = aer_button_callback

        cancel_button = Button(label="Annuler", style=discord.ButtonStyle.red, emoji="❌")

        async def cancel_button_callback(interaction):
            await interaction.response.send_message("Commande annulée.")

        cancel_button.callback = cancel_button_callback

        view = View(timeout=None)
        view.add_item(owner_button)
        view.add_item(fans_dream_team_button)
        view.add_item(aer_button)

        # Crée un embed
        embed = discord.Embed(title='__Please describe your issue or request here :__\n', color=discord.Color.green(), description=
                            """
                            React with 👑 to open a ticket for **Owner**\n
                            React with 🫂 to open a ticket for **Fan Dream Team's**\n
                            React with 🛡️ to open a ticket for **AER**\n
                            """)

        embed.set_footer(text=bot.user.name, icon_url=bot.user.avatar)

        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send("You must use this command in the support channel.")

ticket_counter = 1

@bot.event
async def on_raw_reaction_add(ctx):
    global ticket_counter

    guild = bot.get_guild(ctx.guild_id)
    member = guild.get_member(ctx.user_id)

    if member == bot.user:
        return

    if ctx.channel_id == SUPPORT_CHANNEL_ID:
        ticket_category = discord.utils.get(guild.categories, name="Tickets")
        if not ticket_category:
            ticket_category = await guild.create_category("Tickets")

        ticket_channel_name = f'ticket-{ticket_counter}-{member.display_name}'

        ticket_channel = await ticket_category.create_text_channel(ticket_channel_name)

        ticket_counter += 1

        support_channel = guild.get_channel(SUPPORT_CHANNEL_ID)
        if support_channel:
            await support_channel.send(f"Ticket created in {ticket_channel.mention}")

        await create_ticket_embed(ticket_channel)

# Define create_ticket_embed outside of the event function
def create_ticket_embed(ticket_channel):
    embed = discord.Embed(color=discord.Color.green(), description=f"""
        Your ticket channel has been created!
        React with ❌ to close this ticket
        React with 🔒 to lock this ticket
    """)

@send_message.error
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

@bot.event
async def on_raw_reaction_add(payload):
    global ticket_counter

    if payload.member.bot:
        return
    
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if payload.emoji.name == '❌':
        await message.channel.set_permissions(payload.member, read_messages=False, send_messages=False)
        await message.channel.send(f"{member.mention} has closed this ticket.")
        await message.remove_reaction('❌', payload.member)  
  
    if payload.emoji.name == '🔒':
        await message.channel.set_permissions(payload.member, read_messages=True, send_messages=False)
        await message.channel.send(f"{member.mention} has lock this ticket.")
        await message.remove_reaction('🔒', payload.member)

    if payload.emoji.name == '🔓':
        allowed_roles = ["@root", "GOAT 🐐"]
        has_allowed_role = any(role.name in allowed_roles for role in member.roles)
        if has_allowed_role:
            await message.channel.set_permissions(payload.member, read_messages=True, send_messages=True)
            await message.channel.send(f"{member.mention} successfully unlocked this ticket.")
        else:
            await message.channel.send("Sorry, you do not have permission to use this command.")
            await message.remove_reaction('🔓', payload.member) 
        
    if payload.emoji.name == '🚫':
        allowed_roles = ["@root", "GOAT 🐐"]
        has_allowed_role = any(role.name in allowed_roles for role in member.roles)
        if has_allowed_role:
            await message.channel.set_permissions(payload.member, read_messages=True, send_messages=False)
            await message.remove_reaction('🚫', payload.member)
            await message.channel.delete()
        else:
            await message.channel.send("Sorry, you do not have permission to use this command.")
            await message.remove_reaction('🚫', payload.member)

# Run the bot
bot.run(bot_token) 