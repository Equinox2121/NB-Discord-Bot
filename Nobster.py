import os
from pickle import NONE
from unicodedata import name
import discord
import discord, asyncio
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
import random as r
from dotenv import load_dotenv
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions, cooldown, BucketType, Bot
import datetime
from datetime import datetime, date
import psutil
import random
from discord import app_commands

#------------------------------------------------Basic Neccesities---------------------------------------------#

# Load Token
load_dotenv(".env")
TOKEN = os.getenv("TOKEN")

# Intents are permissions for the bot that are enabled based on the features necessary to run the bot
client = discord.Client(intents=discord.Intents.default())
bot = commands.Bot(intents=discord.Intents.all(), command_prefix= "-")

# Removes the help command to create a custom help guide
bot.remove_command('help')

# Variables 
nobster_id = 1135757721275215922
usage_roles = ["Owner", "Ownber", "VIP", "Omega Moderator", "Moderator", "Event Manager", "QOTD Host", "Giveaway Manager", "Booster", "Pog Champion", "Event Champion", "Legend", "Elite", "Master", "Former Staff"] # Only members with these roles can use the bot
display_roles = ["<@&909616995538984980>", "<@&913997089489424414>", "<@&919337454123769886>", "<@&923291001131532338>", "<@&946507980059320420>", "<@&925832252032696370>", "<@&944107475081236511>", "<@&961792168652058714>", "<@&976565784727916564>", "<@&909901250466820176>", "<@&909901180551962694>", "<@&945842286766473266>", "<@&947943994179068005>"] # Display these roles that are obtainable at bottom of help command

# Channels
channel_feed_id = 1144453230156329030         #1142188833933365390
channel_dm_id = 1144453432627966042           #1142188865789108354
channel_chat_id = 1144453473321091223         #1142188903059701894

#------------------------------------------------Start Up------------------------------------------------------#
# Bot activity status and custom status
@bot.event
async def on_ready():
    print("Bot is online")

#------------------------------------------------Events------------------------------------------------------#

# DM Recieved Section
@bot.event
async def on_message(message):

    # Redirect all dms sent to bot to Discord channel
    if isinstance(message.channel, discord.DMChannel):
        dm_channel = bot.get_channel(channel_dm_id)     #-----> DM Channel
        feed_channel = bot.get_channel(channel_feed_id)     #-----> FEED Channel
        log_author_pfp = message.author.display_avatar # Author's pfp

        # Don't log if message author is bot
        if message.author.id == nobster_id:
            await bot.process_commands(message) # Commands fix
            pass

        else:
            # Embed for messages received
            mail_embed = discord.Embed(title = "📮 DM Received", colour = discord.Color.from_rgb(226,226,226)) # Title, Color
            mail_embed.add_field(name = f"DM received from {message.author.name}", value = (f"{message.content}")) # Show the content of the DM with author's name
            mail_embed.set_thumbnail(url=f"{log_author_pfp}") # Big Image in top right of embed
            mail_embed.set_footer(text=f"ID: {message.author.id}") # Author's ID in footer
            mail_embed.timestamp = datetime.now() # Timestamp of when event occured

            # Attachments fix
            if message.attachments:
                if len(message.attachments) == 1:
                    
                    # Check to see if it can be added to embed (image section)
                    if message.attachments[0].url.endswith(('.jpg', '.png', '.jpeg', '.gif')):
                        mail_embed.set_image(url=message.attachments[0].url)
                    # Wrong file format for embed
                    else:
                        mail_embed.add_field(name="", value = f"Attachment: \n{message.attachments[0].url}", inline = False) # Show any attachments
                # Up to 5 attachments logged
                # More than 1 image attched to message
                elif len(message.attachments) == 2:
                    mail_embed.add_field(name = "", value = f"Attachments: \n1. {message.attachments[0].url}\n2. {message.attachments[1].url}", inline = False) # Show any attachments
                # More than 2 images attched to message
                elif len(message.attachments) == 3:
                    mail_embed.add_field(name = "", value = f"Attachments: \n1. {message.attachments[0].url}\n2. {message.attachments[1].url}\n3. {message.attachments[2].url}", inline = False) # Show any attachments
                # More than 3 images attched to message
                elif len(message.attachments) == 4:
                    mail_embed.add_field(name = "", value = f"Attachments: \n1. {message.attachments[0].url}\n2. {message.attachments[1].url}\n3. {message.attachments[2].url}\n4. {message.attachments[3].url}", inline = False) # Show any attachments
                # More than 4 images attched to message
                elif len(message.attachments) == 5:
                    mail_embed.add_field(name = "", value = f"Attachments: \n1. {message.attachments[0].url}\n2. {message.attachments[1].url}\n3. {message.attachments[2].url}\n4. {message.attachments[3].url}\n5. {message.attachments[4].url}", inline = False) # Show any attachments

                # Send out to channels
                await dm_channel.send(embed = mail_embed) # send to dm channel
                await feed_channel.send(embed = mail_embed) # send to feed channel
                await bot.process_commands(message) # Commands fix

            # No attachments - send out to channels
            else:
                await dm_channel.send(embed = mail_embed) # send to dm channel
                await feed_channel.send(embed = mail_embed) # send to feed channel
                await bot.process_commands(message) # Commands fix
    
    # Ignore Solstice commands prefix -eq
    elif "-eq" in message.content:
        return

    # Finish off section with run commands (always at end of section)
    else:
        await bot.process_commands(message) # Commands fix

#------------------------------------------------Commands------------------------------------------------------#

# Send a member a DM     -dm <@user> <message>
@bot.command(pass_context = True)
@commands.has_any_role(*usage_roles)
# Cooldown settings, 2 uses in 10 seconds per user
@commands.cooldown(2, 10, commands.BucketType.user)
async def dm(ctx, user: discord.User, *, message):
    chat_channel = bot.get_channel(channel_chat_id)     #-----> Chat Channel
    await ctx.message.delete()
    await user.send(message)
    s_sent = await chat_channel.send(f"**{(ctx.author.name).capitalize()} succesfully sent a dm to {(user.name).capitalize()}**")
    # Delete confirmation
    await asyncio.sleep(60)
    await s_sent.delete()

    # Send embed to dm channel
    dm_channel = bot.get_channel(channel_dm_id)  
    dm_embed = discord.Embed(title = "📧 Dm Sent", colour = 0x3498db) # Color, could add Description and Title
    dm_embed.add_field(name = f"DM sent by Nobster to {user.name}", value = (f"{message}")) # Show what was sent in dm
    dm_embed.set_thumbnail(url= "https://cdn.discordapp.com/attachments/935672317512650812/1144812438638829638/nobster_pfp.png") # Big Image in top right of embed (Solstice's PFP)
    dm_embed.set_footer(text=f"ID: {user.id}") # User's ID in footer
    dm_embed.timestamp = datetime.now() # Timestamp of when event occured
    await dm_channel.send(embed = dm_embed)

    # Send embed to feed channel 
    log_author_pfp = ctx.author.display_avatar # Command author's pfp
    log_msg_sent_channel = ctx.channel.id # Channel command was sent in
    feed_channel = bot.get_channel(channel_feed_id)  
    feed_embed = discord.Embed(title = "📧 Dm Sent", colour = 0x3498db) # Color, could add Description and Title
    feed_embed.add_field(name = f"DM sent by {ctx.message.author.name} through Nobster", value = f"Command was used in <#{log_msg_sent_channel}>", inline = False)
    feed_embed.add_field(name = f"Message sent to {user.name}:", value = (f"{message}"), inline = False) # Show what was sent in dm
    #print (f"{str(log_author_pfp)}") # idk why but makes it work (dont remove)
    feed_embed.set_thumbnail(url= f"{str(log_author_pfp)}") # Big Image in top right of embed
    feed_embed.set_footer(text=f"ID: {ctx.author.id}") # Author's ID in footer
    feed_embed.timestamp = datetime.now() # Timestamp of when event occured
    await feed_channel.send(embed = feed_embed)

    # Delete confirmation
    await asyncio.sleep(7.5)
    await s_sent.delete()

# Set a Playing status on bot     -play <message>
@bot.command(pass_context = True)
@commands.has_any_role(*usage_roles)
# Cooldown settings, 2 uses in 10 seconds per user
@commands.cooldown(2, 10, commands.BucketType.user)
async def play(ctx, *message):
    await ctx.message.delete()
    message = str("{}".format(" ".join(message)))
    await bot.change_presence(status=discord.Status.online, activity = discord.Game(name=f"{str(message)}"))
    s_sent = await ctx.send(f"Changed bot activity to **Playing {message}**")
    #print(f"{message}")

    # Send embed to feed channel 
    log_author_pfp = ctx.author.display_avatar # Command author's pfp
    log_msg_sent_channel = ctx.channel.id # Channel command was sent in
    feed_channel = bot.get_channel(channel_feed_id)  
    feed_embed = discord.Embed(title = "Activity Changed", colour = discord.Color.from_rgb(39,219,99)) # Color, could add Description and Title
    feed_embed.add_field(name = f"Nobster's activity status was changed by {ctx.message.author.name}", value = f"Command was used in <#{log_msg_sent_channel}>", inline = False)
    feed_embed.add_field(name = f"Activity status changed to:", value = f"Playing {message}", inline = False)
    feed_embed.set_thumbnail(url= f"{str(log_author_pfp)}") # Big Image in top right of embed
    feed_embed.set_footer(text=f"ID: {ctx.author.id}") # Author's ID in footer
    feed_embed.timestamp = datetime.now() # Timestamp of when event occured
    await feed_channel.send(embed = feed_embed)

    # Delete confirmation
    await asyncio.sleep(7.5)
    await s_sent.delete()

# Set a Watching status on bot     -watch <message>
@bot.command(pass_context = True)
@commands.has_any_role(*usage_roles)
# Cooldown settings, 2 uses in 10 seconds per user
@commands.cooldown(2, 10, commands.BucketType.user)
async def watch(ctx, *message):
    await ctx.message.delete()
    message = str("{}".format(" ".join(message)))
    await bot.change_presence(status=discord.Status.online, activity = discord.Activity(type=discord.ActivityType.watching, name=f"{str(message)}"))
    s_sent = await ctx.send(f"Changed bot activity to **Watching {message}**")
    #print(f"{message}")

    # Send embed to feed channel 
    log_author_pfp = ctx.author.display_avatar # Command author's pfp
    log_msg_sent_channel = ctx.channel.id # Channel command was sent in
    feed_channel = bot.get_channel(channel_feed_id)  
    feed_embed = discord.Embed(title = "Activity Changed", colour = discord.Color.from_rgb(39,219,99)) # Color, could add Description and Title
    feed_embed.add_field(name = f"Nobster's activity status was changed by {ctx.message.author.name}", value = f"Command was used in <#{log_msg_sent_channel}>", inline = False)
    feed_embed.add_field(name = f"Activity status changed to:", value = f"Watching {message}", inline = False)
    feed_embed.set_thumbnail(url= f"{str(log_author_pfp)}") # Big Image in top right of embed
    feed_embed.set_footer(text=f"ID: {ctx.author.id}") # Author's ID in footer
    feed_embed.timestamp = datetime.now() # Timestamp of when event occured
    await feed_channel.send(embed = feed_embed)

    # Delete confirmation
    await asyncio.sleep(7.5)
    await s_sent.delete()

# Set a Listening status on bot     -listen <message>
@bot.command(pass_context = True)
@commands.has_any_role(*usage_roles)
# Cooldown settings, 2 uses in 10 seconds per user
@commands.cooldown(2, 10, commands.BucketType.user)
async def listen(ctx, *message):
    await ctx.message.delete()
    message = str("{}".format(" ".join(message)))
    await bot.change_presence(status=discord.Status.online, activity = discord.Activity(type=discord.ActivityType.listening, name=f"{str(message)}"))
    s_sent = await ctx.send(f"Changed bot activity to **Listening to {message}**")
    #print(f"{message}")

    # Send embed to feed channel 
    log_author_pfp = ctx.author.display_avatar # Command author's pfp
    log_msg_sent_channel = ctx.channel.id # Channel command was sent in
    feed_channel = bot.get_channel(channel_feed_id)  
    feed_embed = discord.Embed(title = "Activity Changed", colour = discord.Color.from_rgb(39,219,99)) # Color, could add Description and Title
    feed_embed.add_field(name = f"Nobster's activity status was changed by {ctx.message.author.name}", value = f"Command was used in <#{log_msg_sent_channel}>", inline = False)
    feed_embed.add_field(name = f"Activity status changed to:", value = f"Listening to {message}", inline = False)
    feed_embed.set_thumbnail(url= f"{str(log_author_pfp)}") # Big Image in top right of embed
    feed_embed.set_footer(text=f"ID: {ctx.author.id}") # Author's ID in footer
    feed_embed.timestamp = datetime.now() # Timestamp of when event occured
    await feed_channel.send(embed = feed_embed)

    # Delete confirmation
    await asyncio.sleep(7.5)
    await s_sent.delete()

# Set a Streaming status on bot     -stream <link> <message>
@bot.command(pass_context = True)
@commands.has_any_role(*usage_roles)
# Cooldown settings, 2 uses in 10 seconds per user
@commands.cooldown(2, 10, commands.BucketType.user)
async def stream(ctx, link, *message):
    await ctx.message.delete()
    message = str("{}".format(" ".join(message)))
    await bot.change_presence(status=discord.Status.online, activity = discord.Streaming(name=f"{str(message)}", url = str(f"{link}")))
    s_sent = await ctx.send(f"Changed bot activity to **Streaming {message}**")
    #print(f"{message}")

    # Send embed to feed channel 
    log_author_pfp = ctx.author.display_avatar # Command author's pfp
    log_msg_sent_channel = ctx.channel.id # Channel command was sent in
    feed_channel = bot.get_channel(channel_feed_id)  
    feed_embed = discord.Embed(title = "Activity Changed", colour = discord.Color.from_rgb(39,219,99)) # Color, could add Description and Title
    feed_embed.add_field(name = f"Nobster's activity status was changed by {ctx.message.author.name}", value = f"Command was used in <#{log_msg_sent_channel}>", inline = False)
    feed_embed.add_field(name = f"Activity status changed to:", value = f"Streaming {message}", inline = False)
    feed_embed.add_field(name = f"Stream link:", value = f"{link}", inline = False)
    feed_embed.set_thumbnail(url= f"{str(log_author_pfp)}") # Big Image in top right of embed
    feed_embed.set_footer(text=f"ID: {ctx.author.id}") # Author's ID in footer
    feed_embed.timestamp = datetime.now() # Timestamp of when event occured
    await feed_channel.send(embed = feed_embed)

    # Delete confirmation
    await asyncio.sleep(7.5)
    await s_sent.delete()

# Clear status on bot     -remove
@bot.command(pass_context = True)
@commands.has_any_role(*usage_roles)
# Cooldown settings, 2 uses in 10 seconds per user
@commands.cooldown(2, 10, commands.BucketType.user)
async def remove(ctx):
    await ctx.message.delete()
    await bot.change_presence(status=None)
    s_sent = await ctx.send("Removed bot activity status")

    # Send embed to feed channel 
    log_author_pfp = ctx.author.display_avatar # Command author's pfp
    log_msg_sent_channel = ctx.channel.id # Channel command was sent in
    feed_channel = bot.get_channel(channel_feed_id)  
    feed_embed = discord.Embed(title = "🗑️ Activity Removed", colour = discord.Color.from_rgb(39,219,99)) # Color, could add Description and Title
    feed_embed.add_field(name = f"Nobster's activity status was removed by {ctx.message.author.name}", value = f"Command was used in <#{log_msg_sent_channel}>", inline = False)
    feed_embed.set_thumbnail(url= f"{str(log_author_pfp)}") # Big Image in top right of embed
    feed_embed.set_footer(text=f"ID: {ctx.author.id}") # Author's ID in footer
    feed_embed.timestamp = datetime.now() # Timestamp of when event occured
    await feed_channel.send(embed = feed_embed)

    # Delete confirmation
    await asyncio.sleep(7.5)
    await s_sent.delete()

# Change 25 random Members' nicknames to something     -trollnickname <message>
@bot.command()
@commands.has_any_role(*usage_roles)
# Cooldown settings, 2 uses in 20 minutes per guild
@commands.cooldown(2, 1200, commands.BucketType.guild)
async def trollnickname(ctx, *args):
    await ctx.message.delete()
    # Needed to work
    intents = discord.Intents.default()
    intents.members = True
    # Variables
    max_members = 25
    counter = 0
    five_counter = 5
    chosen_members = []
    effected_members = []
    nobster = discord.utils.get(ctx.guild.roles, name="Nobster")
    nickname = str("{}".format(" ".join(args)))
    # Messages stating it's started and the counter
    counter_message = await ctx.send(f"**(🔄 {str(counter)}/{str(max_members)}) Changing 25 random Members' nicknames to __{nickname}__.**")

    # Get 25 random members and add them to list
    while len(chosen_members) != max_members:
        chosen = random.choice(ctx.guild.members)
        # Don't add repeats of members to list
        if chosen in chosen_members:
            pass
        # Don't add people higher than bot
        elif chosen.top_role.position > nobster.position:
            pass
        else:
            chosen_members.append(chosen)
            #print(f'{chosen}')
    
    # Loop to change all member's nicknames
    for member in chosen_members: # loop through every member in the chosen list
        await asyncio.sleep(2) # Keeps bot from rate limiting
        try:
            await member.edit(nick=f'{nickname}') # Change their nickname
            effected_members.append(member.mention)
            counter +=1
        except:
            pass

        # Counter system
        if counter == max_members:
            break
        elif counter >= five_counter:
            await counter_message.edit(content = f"**(🔄 {str(counter)}/{str(max_members)}) Changing 25 random Members' nicknames to __{nickname}__.**")
            # Add 5 more to the five counter
            five_counter += 5
        # Skip every 5
        else:
            pass

        # Loop ends
    await counter_message.edit(content = f"**🔄 Changed {str(counter)} random Members' nicknames to __{nickname}__.**")

    # Send embed to feed channel 
    log_author_pfp = ctx.author.display_avatar # Command author's pfp
    log_msg_sent_channel = ctx.channel.id # Channel command was sent in
    feed_channel = bot.get_channel(channel_feed_id)  
    feed_embed = discord.Embed(title = "🔄 25 Random Nicknames Changed", colour = discord.Color.from_rgb(200,137,255)) # Color, could add Description and Title
    feed_embed.add_field(name = f"{ctx.message.author.name} changed 25 random nicknames to __{nickname}__", value = f"Command was used in <#{log_msg_sent_channel}>", inline = False)
    feed_embed.add_field(name = f"Members effected:", value = (f"{', '.join(effected_members)}"), inline = False) # Show members effected
    #print (f"{str(log_author_pfp)}") # idk why but makes it work (dont remove)
    feed_embed.set_thumbnail(url= f"{str(log_author_pfp)}") # Big Image in top right of embed
    feed_embed.set_footer(text=f"ID: {ctx.author.id}") # Author's ID in footer
    feed_embed.timestamp = datetime.now() # Timestamp of when event occured
    await feed_channel.send(embed = feed_embed)

# Say a message through Nobster command     -say <message>
@bot.command(pass_context = True)
@commands.has_any_role(*usage_roles)
# Cooldown settings, 2 uses in 10 seconds per user
@commands.cooldown(2, 10, commands.BucketType.user)
async def say(ctx, *args):
    await ctx.message.delete()
    msg_sent = await ctx.send("{}".format(" ".join(args)))
    msg_content = msg_sent.content

    # Send embed to feed channel 
    log_author_pfp = ctx.author.display_avatar # Command author's pfp
    log_msg_sent_channel = ctx.channel.id # Channel command was sent in
    feed_channel = bot.get_channel(channel_feed_id)  
    feed_embed = discord.Embed(title = "💬 Say Command", colour = discord.Color.from_rgb(200,137,255)) # Color, could add Description and Title
    feed_embed.add_field(name = f"Nobster reapeated a message from {ctx.message.author.name}", value = f"Command was used in <#{log_msg_sent_channel}>", inline = False)
    feed_embed.add_field(name = f"Message:", value = (f"{msg_content}"), inline = False) # Show what was sent in dm
    #print (f"{str(log_author_pfp)}") # idk why but makes it work (dont remove)
    feed_embed.set_thumbnail(url= f"{str(log_author_pfp)}") # Big Image in top right of embed
    feed_embed.set_footer(text=f"ID: {ctx.author.id}") # Author's ID in footer
    feed_embed.timestamp = datetime.now() # Timestamp of when event occured
    await feed_channel.send(embed = feed_embed)

# Send message through bot command     -send <channel> <message>
@bot.command(pass_context = True)
@commands.has_any_role(*usage_roles)
# Cooldown settings, 2 uses in 10 seconds per user
@commands.cooldown(2, 10, commands.BucketType.user)
async def send(ctx, channel, *args):
    await ctx.message.delete()
    # remove the <#> from channel input
    channel_id = ''.join(filter(str.isdigit, channel))
    #print (f"{channel_id}")
    send_channel = bot.get_channel(int(channel_id))     #-----> Channel
    msg_sent = await send_channel.send("{}".format(" ".join(args)))
    s_sent = await ctx.send(f"Message sent to <#{channel_id}>")
    msg_content = msg_sent.content

    # Send embed to feed channel 
    log_author_pfp = ctx.author.display_avatar # Command author's pfp
    log_msg_sent_channel = ctx.channel.id # Channel command was sent in
    feed_channel = bot.get_channel(channel_feed_id)  
    feed_embed = discord.Embed(title = "📤 Send Command", colour = discord.Color.from_rgb(200,137,255)) # Color, could add Description and Title
    feed_embed.add_field(name = f"Nobster sent a message from {ctx.message.author.name}", value = f"Command was used in <#{log_msg_sent_channel}>", inline = False)
    feed_embed.add_field(name = f"Message sent to #{send_channel}:", value = (f"{msg_content}"), inline = False) # Show what was sent in dm
    #print (f"{str(log_author_pfp)}") # idk why but makes it work (dont remove)
    feed_embed.set_thumbnail(url= f"{str(log_author_pfp)}") # Big Image in top right of embed
    feed_embed.set_footer(text=f"ID: {ctx.author.id}") # Author's ID in footer
    feed_embed.timestamp = datetime.now() # Timestamp of when event occured
    await feed_channel.send(embed = feed_embed)

    # Delete confirmation
    await asyncio.sleep(5)
    await s_sent.delete()

#------------------------------------------------Utility------------------------------------------------------#

# Check bot ping command -ms
@bot.command()
@commands.has_permissions(administrator = True)
async def ms(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title = '', description = (f"**Ping**: {round(bot.latency * 1000)}ms"), colour = discord.Color.from_rgb(255,0,0))
    await ctx.send(embed = embed)

# Check memory command -usage
@bot.command()
@commands.has_permissions(administrator = True)
async def usage(ctx):
    await ctx.message.delete()
    bedem = discord.Embed(title = 'System Resource Usage', description = 'CPU and Memory usage of Nobster', colour = discord.Color.from_rgb(255,0,0))
    bedem.add_field(name = 'CPU Usage', value = f'{psutil.cpu_percent()}%', inline = False)
    bedem.add_field(name = 'Memory Usage', value = f'{psutil.virtual_memory().percent}%', inline = False)
    memory = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    memory = '{:0.1f}'.format(memory)
    bedem.add_field(name = 'Available Memory', value = f'{memory}%', inline = False)
    await ctx.send(embed = bedem)
    bedem.timestamp = datetime.now() # Timestamp of when event occured

#------------------------------------------------List out all Commands Command------------------------------------------------------#

# List out commands and info   -cmds
@bot.command()
@commands.has_any_role(*usage_roles)
# Cooldown settings, 2 uses in 10 seconds per user
@commands.cooldown(2, 10, commands.BucketType.user)
async def cmds(ctx):
    await ctx.message.delete()
    # Info for top of embed 
    log_author_pfp = ctx.author.display_avatar # Command author's pfp
    # Make the roles list look nice
    roles = (", ".join(display_roles))
    # Embeded message
    help = discord.Embed(title = 'Nobster Commands', colour = discord.Color.from_rgb(1,1,1))
    help.set_author(name = f"Made by @Equinox21", icon_url = str(log_author_pfp)) # Author's Name and Pfp at top of embed
    help.add_field(name = '📧 -dm', value = "Send a message through Nobster to another server Member. Full Command: ***-dm <user> <msg>***", inline = True)
    help.add_field(name = '🎲 -play', value = "Change the bot's status to playing something. Full Command: ***-play <msg>***", inline = True)
    help.add_field(name = '👀 -watch', value = "Change the bot's status to watching something. Full Command: ***-watch <msg>***", inline = True)
    help.add_field(name = '🗑️ -remove', value = "Clear the bot's activity status (if it had one). Full Command: ***-clear***", inline = True)
    help.add_field(name = '🎵 -listen', value = "Change the bot's status to listening to something. Full Command: ***-listen <msg>***", inline = True)
    help.add_field(name = '🔴 -stream', value = "Change the bot's status to streaming something. Full Command: ***-stream <stream link> <msg>***", inline = True)
    help.add_field(name = '💬 -say', value = "Get Nobster to repeat exactly what you said in a channel (deletes your message). Full Command: ***-say <msg>***", inline = True)
    help.add_field(name = '🔄 -trollnickname', value = "Change 25 random Member's nicknames to whatever you input. Full Command: ***-trollnickname <msg>***", inline = True)
    help.add_field(name = '📤 -send', value = "Similar to -say, but send the message to a different channel. Full Command: ***-send <channel> <msg>***", inline = True)
    help.add_field(name = '', value = '', inline = False)
    help.add_field(name = '', value = f"Roles allowed to use these commands: {roles}.", inline = False)
    #help.set_footer(text=f"Roles allowed to use these commands: {roles}.") # Author's ID in footer
    await ctx.send(embed = help)

#------------------------------------------------Error Messages------------------------------------------------------#

@bot.event
async def on_command_error(ctx, error):
    print("Running Errors Section")
    # User errors
    # Cooldown error (deletes command)
    if isinstance(error, commands.CommandOnCooldown):
        error_msg_1 = "This command is on cooldown, please try again in {:.0f} seconds".format(error.retry_after)
        await ctx.message.delete()
        await ctx.send(error_msg_1)
        print("Error 1, cooldown")
    # Missing role error (deletes command)
    elif isinstance(error, commands.MissingRole):
        error_msg_2 = "You do not have the role needed to run this command"
        await ctx.message.delete()
        await ctx.send(error_msg_2)
        print("Error 2, missing role")
    # Missing permissions error (deletes command)
    elif isinstance(error, commands.MissingPermissions):
        error_msg_3 = "You do not have the permissions needed to run this command"
        await ctx.message.delete()
        await ctx.send(error_msg_3)
        print("Error 3, missing permissions")
    elif isinstance(error, commands.MissingRequiredArgument):
        error_msg_4 = "You did not provide a required argument needed to run this command"
        await ctx.message.delete()
        await ctx.send(error_msg_4)
        print("Error 4, missing agruement")
    elif isinstance(error, commands.MissingRequiredAttachment):
        error_msg_4 = "You did not provide a required attachment needed to run this command"
        await ctx.message.delete()
        await ctx.send(error_msg_4)
        print("Error 5, missing attachment")

    # Bot errors
    # Bot missing permissions error
    elif isinstance(error, commands.BotMissingPermissions):
        bot_error_msg_1 = "I do not have the permissions needed to run this command"
        await ctx.message.delete()
        await ctx.send(bot_error_msg_1)
        print("Bot Error 1, missing permissions")
    # Bot missing role error
    elif isinstance(error, commands.BotMissingRole):
        bot_error_msg_2 = "I do not have the role needed to run this command"
        await ctx.message.delete()
        await ctx.send(bot_error_msg_2)
        print("Bot Error 2, missing role")

    #else: 
        #s_sent = await ctx.send("ERROR: Make sure you typed the command right and ping Equinox if you need further assistance.")
         # Delete confirmation
        #await asyncio.sleep(7.5)
        #await s_sent.delete()

#------------------------------------------------Run the Bot------------------------------------------------------#

# Run the Bot
bot.run(TOKEN)