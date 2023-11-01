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
            await messages.add_reaction('🔓')

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
            await messages.add_reaction('🔓')


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
            await messages.add_reaction('🔓')

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