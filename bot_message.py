import discord
from discord.ext import commands
from help_all import *

intents = discord.Intents.default()
intents.typing = True
intents.message_content = True
intents.members = True

ticket_counter = 1

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
bot_enabled = True 

send_message_enabled = True

ticket_category_name = "Tickets"

server_id = 1159020670575968371
bot_token = 'MTE2ODQ4MTA4MDY4OTU2OTgxMg.GFavhS.shT-7dgxpjvvAInMB1vaa8Jsq7K7KIpx2h-X_I'

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
                            **🔒** : Lock the ticket\n\n
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

# Message in chanel discord
@bot.command()
async def send_message(ctx, channel_id, repeat_count: int, *, message):
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
async def send_pmessage(ctx, user_id, repeat_count: int, *, message):
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

# Handle command errors
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

# Ticket system
@bot.command()
async def setup_ticket(ctx):
    guild = ctx.guild
    ticket_category = discord.utils.get(guild.categories, name="Tickets")
    
    if not ticket_category:
        ticket_category = await guild.create_category("Tickets")
    
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True)
    }

    ticket_channel = await ticket_category.create_text_channel(f'📬│ticket', overwrites=overwrites)

    ticket_embed = discord.Embed(title='__Please describe your issue or request here :__\n', color=discord.Color.green(), description=
    """
    React with 👑 to open a ticket for **Owner**\n
    React with 🫂 to open a ticket for **Fan Dream Team's**\n
    React with 🛡️ to open a ticket for **AER**\n
    React with 🍹 to get **Party notif**\n
    """)

    ticket_message = await ticket_channel.send(embed=ticket_embed)

    await ticket_message.add_reaction('👑')
    await ticket_message.add_reaction('🫂')
    await ticket_message.add_reaction('🛡️')
    await ticket_message.add_reaction('🍹')

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


    if payload.emoji.name == '👑':
        guild = bot.get_guild(payload.guild_id)
        ticket_category = discord.utils.get(guild.categories, name="Tickets")
    

        if not ticket_category:
            ticket_category = await guild.create_category("Tickets")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            payload.member: discord.PermissionOverwrite(read_messages=True)
        }

        try:
            new_channel = await guild.create_text_channel(name=f"Ticket-{ticket_counter}-[{payload.member.name}]", category=ticket_category, overwrites=overwrites)
        except Exception as e:
            print(f"An error occurred while creating the ticket channel: {e}")
        else:
            message = await new_channel.send(f"<@&1159222810045055076>")
            await message.delete()
            embed = discord.Embed(title='__A new ticket was created__\n', color=discord.Color.blue(), description=f"""\n
            {payload.member.mention}, your ticket channel has been created!\n
            React with ❌ to close this ticket\n
            React with 🔒 to lock this ticket\n
            """)
            messages = await new_channel.send(embed=embed)
            await messages.add_reaction('❌')
            await messages.add_reaction('🔒')
            await messages.add_reaction('🚫')

            await new_channel.set_permissions(payload.member, read_messages=True, send_messages=True)
            await payload.member.send(f"Your ticket channel has been created in {new_channel.mention}")
            await payload.member.send(f"React with ❌ to close this ticket")
            await payload.member.send(f"React with 🔒 to lock this ticket")

            channel = bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            member = guild.get_member(payload.user_id)
            await message.remove_reaction('👑', member)

        ticket_counter += 1


    if payload.emoji.name == '🫂':
        guild = bot.get_guild(payload.guild_id)
        ticket_category = discord.utils.get(guild.categories, name="Tickets")
    

        if not ticket_category:
            ticket_category = await guild.create_category("Tickets")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            payload.member: discord.PermissionOverwrite(read_messages=True)
        }

        try:
            new_channel = await guild.create_text_channel(name=f"Ticket-{ticket_counter}-[{payload.member.name}]", category=ticket_category, overwrites=overwrites)
        except Exception as e:
            print(f"An error occurred while creating the ticket channel: {e}")
        else:
            message = await new_channel.send(f"<@&1159222810045055076>")
            await message.delete()
            embed = discord.Embed(title='__A new ticket was created__\n', color=discord.Color.blue(), description=f"""\n
            {payload.member.mention}, your ticket channel has been created!\n
            React with ❌ to close this ticket\n
            React with 🔒 to lock this ticket\n
            """)
            messages = await new_channel.send(embed=embed)
            await messages.add_reaction('❌')
            await messages.add_reaction('🔒')
            await messages.add_reaction('🚫')


            await new_channel.set_permissions(payload.member, read_messages=True, send_messages=True)
            await payload.member.send(f"Your ticket channel has been created in {new_channel.mention}")
            await payload.member.send(f"React with ❌ to close this ticket")
            await payload.member.send(f"React with 🔒 to lock this ticket")

            channel = bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            member = guild.get_member(payload.user_id)
            await message.remove_reaction('🫂', member)

        ticket_counter += 1


    if payload.emoji.name == '🛡️':
        guild = bot.get_guild(payload.guild_id)
        ticket_category = discord.utils.get(guild.categories, name="Tickets")
    

        if not ticket_category:
            ticket_category = await guild.create_category("Tickets")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            payload.member: discord.PermissionOverwrite(read_messages=True)
        }

        try:
            new_channel = await guild.create_text_channel(name=f"Ticket-{ticket_counter}-[{payload.member.name}]", category=ticket_category, overwrites=overwrites)
        except Exception as e:
            print(f"An error occurred while creating the ticket channel: {e}")
        else:
            message = await new_channel.send(f"<@&1159222810045055076>")
            await message.delete()
            embed = discord.Embed(title='__A new ticket was created__\n', color=discord.Color.blue(), description=f"""\n
            {payload.member.mention}, your ticket channel has been created!\n
            React with ❌ to close this ticket\n
            React with 🔒 to lock this ticket\n
            """)
            messages = await new_channel.send(embed=embed)
            await messages.add_reaction('❌')    
            await messages.add_reaction('🔒')
            await messages.add_reaction('🚫')

            await new_channel.set_permissions(payload.member, read_messages=True, send_messages=True)
            await payload.member.send(f"Your ticket channel has been created in {new_channel.mention}")
            await payload.member.send(f"React with ❌ to close this ticket")
            await payload.member.send(f"React with 🔒 to lock this ticket")

            channel = bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            member = guild.get_member(payload.user_id)
            await message.remove_reaction('🛡️', member)

        ticket_counter += 1

    if payload.emoji.name == '🍹':
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role_name = "🍹 || Party Notif"
        role = discord.utils.get(guild.roles, name=role_name)

        if role is not None:
            await member.add_roles(role)

            channel = bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.remove_reaction('🍹', member)
        else:
            print("Role not found.")

# Run the bot
bot.run(bot_token) 