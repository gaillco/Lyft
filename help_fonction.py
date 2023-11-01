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


@bot.command()
async def help_staff(ctx):
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

@bot.command()
async def help_user(ctx):
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

@bot.command()
async def help_ticket_fonction(ctx):
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