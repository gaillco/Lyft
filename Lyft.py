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
    if any(word in message.content for word in ["discord.gg/","//discord", "discord.com/invite/", "discordapp.com/invite/", "discord.me/", "discord.io/", "discord.tk/", "discordlist.net/", "discord.ly/", "discord.link/", "disboard.org/", "discord.gg"]):
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
    if before.guild is not None and before.guild.id == SOURCE_SERVER_ID:
        log_channel = bot.get_channel(DESTINATION_CHANNEL_ID_edited)
        if log_channel:
            if before.author == bot.user:
                await log_channel.send(f"Message edited by the bot {bot.user.name} (ID: {before.author.id})")
            else:
                author_name = before.author.display_name if before.author else "Unknown User"
                await log_channel.send(f"Message edited by {author_name}\nID = {before.author.id}\nContent of the message before : '**{before.content}**'\nContent of the message after : '**{after.content}**'\nIn {before.channel.mention}")

# Log deleted messages 
@bot.event
async def on_message_delete(message):
    if message.guild is not None and message.guild.id == SOURCE_SERVER_ID:
        log_channel = bot.get_channel(DESTINATION_CHANNEL_ID_delete)
        if log_channel:
            author_name = message.author.display_name if message.author else "Unknown User"
            if message.author.id == bot.user.id:
                await log_channel.send(f"Message deleted by the bot {bot.user.name} (ID: {message.author.id})\nContent of the message: '**{message.content}**'")
            else:
                await log_channel.send(f"----------------------------\nMessage deleted by {author_name}\nID = {message.author.id}\nContent of the message: '**{message.content}**'\nIn {message.channel.mention}\n----------------------------")

# Bot activation
@bot.tree.command(name="toggle", description="Activate or desactivate the bot")
async def toggle(interaction):
    ctx = await bot.get_context(interaction)
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        global bot_enabled
        bot_enabled = not bot_enabled
        status = "activated" if bot_enabled else "disabled"
        await ctx.send(f"The bot is now {status}.")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.")

# Dropdown for grade selection
class GradeSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Grade 1", description="Select Grade 1", value="1"),
            discord.SelectOption(label="Grade 2", description="Select Grade 2", value="2"),
            discord.SelectOption(label="Grade 3", description="Select Grade 3", value="3"),
            # Add more grades as options here
        ]
        super().__init__(placeholder="Choose your grade...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'You selected {self.values[0]}', ephemeral=True)

# Command to initiate the grade selection process
class GradeSelectView(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(GradeSelect())

    @ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=None)

@bot.tree.command(name="select_grade", description="Select your grade")
async def select_grade(interaction: discord.Interaction):
    await interaction.response.send_message("Please select your grade:", view=GradeSelectView(), ephemeral=True)

async def has_any_role_check_nv1(interaction: discord.Interaction) -> bool:
    role_names = {"@root", "👑  || Owner", "GOAT 🐐", "🫂 || Fan Dream Team", "🛡️ || AER"}
    user_roles = {role.name for role in interaction.user.roles}
    return any(role in user_roles for role in role_names)

# Check who is the owner
@bot.tree.command(name="is_owner", description="To display who is the owner")
async def is_owner(interaction):
    ctx = await bot.get_context(interaction)
    allowed_roles = ["🫂 || Fan Dream Team", "🛡️ || AER", "GOAT 🐐","👑  || Owner", "<@root>"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        guild = ctx.guild
        author = ctx.author

        if guild and guild.owner == author:
            await ctx.send(f'{author.display_name} is the owner of this server!', ephemeral=True)
        else:
            await ctx.send(f'{author.display_name} is not the owner of this server. The owner is {guild.owner.display_name} (ID : {guild.owner.id}).', ephemeral=True)
    else:
        await ctx.send("Sorry, you do not have permission to use this command.", ephemeral=True)


# List of available orders for user
@bot.tree.command(name="help", description="Displays the user list of commands")
async def help(interaction):
    ctx = await bot.get_context(interaction)

    allowed_roles = ["🫂 || Fan Dream Team", "🛡️ || AER", "GOAT 🐐", "👑  || Owner", "@root"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        embed = discord.Embed(title='__List of available orders :__\n', color=discord.Color.blue(), description="""
                        **/help** : Displays the user list of commands\n
                        **/help_all** : Displays the staff list of commands\n
                        **/help_ticket** : Displays the action for the ticket\n
                        **/is_owner** : To display who is the owner\n
                        **/send_pmessage** : Sends messages to a user on the discord server, command to be followed : ```!send_pmessage <user_id> <repeat_count> <message>```\n""", ephemeral=True
                        )
        roles = [role.name for role in ctx.author.roles]
        roles_text = ', '.join(roles)
                
        if ctx.author.avatar is not None:
            embed.set_footer(text=f"{ctx.author.name} - [ {roles_text} ] - ", icon_url=ctx.author.avatar.url)
        else:
            embed.set_footer(text=f"{ctx.author.name} - [ {roles_text} ] - ")
    else:
        await ctx.send("Sorry, you do not have permission to use this command.", ephemeral=True)

    await ctx.send(embed=embed)

# List of available orders for staff
@bot.tree.command(name="help_all", description="Displays the staff list of commands")
async def help_all(interaction):
    ctx = await bot.get_context(interaction)

    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        embed = discord.Embed(title='__List of available orders :__\n', color=discord.Color.blue(), description="""
                        **/help** : Displays the user list of commands\n
                        **/help_all** : Displays the staff list of commands\n
                        **/help_ticket** : Displays the action for the ticket\n
                        **/toggle**: Activate or desactivate the bot\n
                        **/is_owner** : To display who is the owner\n
                        **/all** : Delete all messages in the chanel discord\n
                        **/stop_send** : Disable message sending to chanel discord\n
                        **/start_send** : Enable message sending to chanel discord\n
                        **/delc** : Delete the chanel discord\n
                        **/send_message** : Send messages in a discord chanel, command to be followed : ```!send_message <channel_id> <repeat_count> <message>```\n
                        **/send_pmessage** : Sends messages to a user on the discord server, command to be followed : ```!send_pmessage <user_id> <repeat_count> <message>```\n
                        **/clear** : Delete messages in a chanel discord, command to be followed : ```!clear <amount>```\n
                        """, ephemeral=True)
        roles = [role.name for role in ctx.author.roles]
        roles_text = ', '.join(roles)

        if ctx.author.avatar is not None:
            embed.set_footer(text=f"{ctx.author.name} - [ {roles_text} ] - ", icon_url=ctx.author.avatar.url)
        else:
            embed.set_footer(text=f"{ctx.author.name} - [ {roles_text} ] - ")

    else:
        await ctx.send("Sorry, you do not have permission to use this command.", ephemeral=True)

    await ctx.send(embed=embed)

# List of available orders for ticket
@bot.tree.command(name="help_ticket", description="Displays the ticket list of commands")
async def help_ticket(interaction):
    ctx = await bot.get_context(interaction)
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]

    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)

    if has_allowed_role:
        embed = discord.Embed(title='__List of commande for ticket__\n', color=discord.Color.blue(), description="""
                            **/setup_ticket** : Create the setup for ticket\n
                            **🚫** : Only for admin, delete the ticket\n
                            **❌** : Close the ticket\n
                            **🔒** : Lock the ticket\n
                            **🔓** : Unlock the ticket\n
                            """, ephemeral=True)
        roles = [role.name for role in ctx.author.roles]
        roles_text = ', '.join(roles)

        if ctx.author.avatar is not None:
            embed.set_footer(text=f"{ctx.author.name} - [ {roles_text} ] - ", icon_url=ctx.author.avatar.url)
        else:
            embed.set_footer(text=f"{ctx.author.name} - [ {roles_text} ] - ")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Sorry, you do not have permission to use this command.", ephemeral=True)

# Message in chanel discord
@bot.tree.command(name="send_message", description="Send a message to a channel.")
@app_commands.checks.has_any_role("@root", "👑  || Owner", "GOAT 🐐", "🫂 || Fan Dream Team", "🛡️ || AER")
@app_commands.check(has_any_role_check_nv1) 
async def send_message(interaction: discord.Interaction, channel: discord.TextChannel, repeat_count: int, message: str):
    try:
        await interaction.response.defer(ephemeral=True)

        if channel:
            for _ in range(repeat_count):
                await channel.send(message)
            await interaction.followup.send(f"{repeat_count} messages sent to {channel.mention}.", ephemeral=True)
        else:
            await interaction.followup.send("Channel not found or you do not have permission to send messages to this channel.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)


# Message to user
@bot.tree.command(name="send_pmessage", description="Send a private message to a user.")
@app_commands.checks.has_any_role("@root", "👑  || Owner", "GOAT 🐐", "🫂 || Fan Dream Team", "🛡️ || AER")
@app_commands.check(has_any_role_check_nv1) 
async def send_pmessage(interaction: discord.Interaction, user: discord.User, repeat_count: int, message: str):
    try:
        await interaction.response.defer(ephemeral=True)

        await user.create_dm()
        for _ in range(repeat_count):
            await user.send(message)

        await interaction.followup.send(f"{repeat_count} messages sent to {user.mention}.", ephemeral=True)
    except PermissionError:
        await interaction.followup.send("Sorry, you do not have permission to use this command.", ephemeral=True)


# Delete channel
@bot.tree.command(name="delc", description="Delete the chanel discord")
async def delc(interaction):
    ctx = await bot.get_context(interaction)
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        try:
            await ctx.channel.delete()
        except discord.Forbidden:
            await ctx.send("I don't have the permission to delete this channel.", ephemeral=True)
        except discord.HTTPException:
            await ctx.send("An error occurred while deleting the channel.", ephemeral=True)
    else:
        await ctx.send("Sorry, you do not have permission to use this command.", ephemeral=True)

# Clear messages
@bot.tree.command(name="clear", description="Delete messages in a channel on Discord")
@app_commands.checks.has_any_role("@root", "👑  || Owner", "GOAT 🐐", "🫂 || Fan Dream Team", "🛡️ || AER")
@app_commands.check(has_any_role_check_nv1)
async def clear(interaction: discord.Interaction, amount: int):
    if amount <= 0:
        await interaction.response.send_message("Please specify a valid number of messages to delete.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    channel = interaction.channel
    if isinstance(channel, discord.TextChannel):
        deleted_messages = await channel.purge(limit=amount)
        await interaction.followup.send(f"{len(deleted_messages)} messages have been deleted.", ephemeral=True)
    else:
        await interaction.followup.send("This command can only be used in text channels.", ephemeral=True)


# Clear all messages
@bot.tree.command(name="all", description="Delete all messages in the chanel discord")
async def all(interaction):
    ctx = await bot.get_context(interaction)
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        await ctx.channel.purge()
        await ctx.send("All messages have been deleted.", ephemeral=True)
    else:
        await ctx.send("Sorry, you do not have permission to use this command.", ephemeral=True)

# Kick members
@bot.tree.command(name="kick", description="Kick a member")
@app_commands.checks.has_any_role("@root", "👑  || Owner", "GOAT 🐐", "🫂 || Fan Dream Team", "🛡️ || AER")
@app_commands.check(has_any_role_check_nv1) 
async def kick(interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
    try:
        dm_message = f"You have been kicked from {interaction.guild.name}."
        if reason:
            dm_message += f" Reason: {reason}"
        try:
            await member.send(dm_message)
        except discord.errors.HTTPException:
            pass

        await member.kick(reason=reason)

        log_channel_id = LOG__KICK_CHANNEL_ID
        other_guild_id = SOURCE_SERVER_ID

        log_guild = bot.get_guild(other_guild_id)
        log_channel = log_guild.get_channel(log_channel_id) if log_guild else None

        if log_channel:
            try:
                await log_channel.send(f"{member.display_name} has been kicked by {interaction.author.display_name}. Reason: {reason if reason else 'No reason provided'}")
            except Exception as e:
                print(f"Failed to send message to log channel: {e}")
        else:
            print("Log channel not found")


        await interaction.response.send_message(f"{member.display_name} has been kicked.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I do not have permission to kick this user.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)




# Disable messages
@bot.tree.command(name="stop_send", description="Disable message sending to chanel discord")
async def stop_send(interaction):
    ctx = await bot.get_context(interaction)
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        global send_message_enabled
        send_message_enabled = False
        await ctx.send("The send_message command has been disabled.", ephemeral=True)
    else:
        await ctx.send("Sorry, you do not have permission to use this command.", ephemeral=True)


# Enabled messages
@bot.tree.command(name="start_send", description="Enable message sending to chanel discord")
async def start_send(interaction):
    ctx = await bot.get_context(interaction)
    allowed_roles = ["@root", "👑  || Owner", "GOAT 🐐"]
    
    has_allowed_role = any(role.name in allowed_roles for role in ctx.author.roles)
    
    if has_allowed_role:
        global send_message_enabled
        send_message_enabled = True
        await ctx.send("The send_message command has been enabled.", ephemeral=True)
    else:
        await ctx.send("Sorry, you do not have permission to use this command.", ephemeral=True)

# Create ticket
@bot.tree.command(name="setup_ticket", description="setup ticket for ticket")
async def setup_ticket(interaction):
    ctx = await bot.get_context(interaction)
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