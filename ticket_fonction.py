import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.typing = True
intents.message_content = True
intents.members = True
intents.guilds = True

ticket_counter = 1

bot = commands.Bot(command_prefix='!', intents=intents)
bot_enabled = True 

send_message_enabled = True

SUPPORT_CHANNEL_ID = 1169341227548807338

ticket_category_name = "Tickets"

@bot.command()
async def setup_ticket_fonction(ctx):
    guild = ctx.guild
    member = ctx.author

    if ctx.channel.id == SUPPORT_CHANNEL_ID:
        # Crée un bouton pour créer un ticket
        owner_button = Button(label="Owner", style=discord.ButtonStyle.green, emoji="👑")

        async def owner_button_callback(interaction):
            ticket_category = discord.utils.get(guild.categories, name="Tickets")
            if not ticket_category:
                ticket_category = await guild.create_category("Tickets")

            ticket_channel = await ticket_category.create_text_channel(f'ticket-{member.display_name}')
            await ticket_channel.send(embed=create_ticket_embed())

            await interaction.response.send_message(f"Ticket créé dans {ticket_channel.mention}", ephemeral=True)

        owner_button.callback = owner_button_callback

        # Crée un bouton pour créer un ticket
        fans_dream_team_button = Button(label="Fan Dream Team's", style=discord.ButtonStyle.green, emoji="🫂")

        async def fans_dream_team_button_callback(interaction):
            ticket_category = discord.utils.get(guild.categories, name="Tickets")
            if not ticket_category:
                ticket_category = await guild.create_category("Tickets")

            ticket_channel = await ticket_category.create_text_channel(f'ticket-{member.display_name}')
            await ticket_channel.send(embed=create_ticket_embed())

            await interaction.response.send_message(f"Ticket créé dans {ticket_channel.mention}")

        fans_dream_team_button.callback = fans_dream_team_button_callback
           
        # Crée un bouton pour créer un ticket
        aer_button = Button(label="AER", style=discord.ButtonStyle.green, emoji="🛡️")

        async def aer_button_callback(interaction):
            ticket_category = discord.utils.get(guild.categories, name="Tickets")
            if not ticket_category:
                ticket_category = await guild.create_category("Tickets")

            ticket_channel = await ticket_category.create_text_channel(f'ticket-{member.display_name}')
            await ticket_channel.send(embed=create_ticket_embed())

            await interaction.response.send_message(f"Ticket créé dans {ticket_channel.mention}")

        aer_button.callback = aer_button_callback

        # Crée un bouton pour annuler la commande
        cancel_button = Button(label="Annuler", style=discord.ButtonStyle.red, emoji="❌")

        async def cancel_button_callback(interaction):
            await interaction.response.send_message("Commande annulée.")

        cancel_button.callback = cancel_button_callback

        # Crée une vue avec les deux boutons
        view = View()
        view.add_item(owner_button)
        view.add_item(fans_dream_team_button)
        view.add_item(aer_button)
        # view.add_item(fiesta_button)

        # Crée un embed
        embed = discord.Embed(title='__Please describe your issue or request here :__\n', color=discord.Color.green(), description=
                            """
                            React with 👑 to open a ticket for **Owner**\n
                            React with 🫂 to open a ticket for **Fan Dream Team's**\n
                            React with 🛡️ to open a ticket for **AER**\n
                            React with 🍹 to get **Party notif**\n
                            """)
        embed.set_footer(text=bot.user.name, icon_url=bot.user.avatar)

        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send("Vous devez utiliser cette commande dans le canal de support.")

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





