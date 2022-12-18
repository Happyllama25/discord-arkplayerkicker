import disnake
from rcon.source import Client
from disnake.ext import commands
from enum import Enum


bot = commands.Bot(command_prefix=disnake.ext.commands.when_mentioned,test_guilds=[<your-guild-ID-here>])



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")


@bot.slash_command(description="Sends bot latency")
async def ping(inter: disnake.ApplicationCommandInteraction):
    await inter.response.send_message(f'{round(bot.latency * 1000)}ms')

    
#In this context, 'Player1' will show up as an option in discord when the command is written
#Replace 'SteamID' with the respective players' SteamID
class Users(str, Enum): 
    Player1 = 'SteamID1'
    Player2 = 'SteamID2'
    Player3 = 'SteamID3'
    
@bot.slash_command(description="Lists connected players")
# @commands.has_role(733408652077170785) #Optional, you can specify an admin role ID here to only allow certain roles to perform the command
async def players(inter: disnake.ApplicationCommandInteraction):
    with Client('<Server IP>', <RCON Port>, passwd='<AdminPassword>') as client:
        response = client.run('listplayers')
        await inter.response.send_message(f'{response}')

@bot.slash_command(description="Kicks a player from the ARK Server")
# @commands.has_role(733408652077170785) #Optional, you can specify an admin role ID here to only allow certain roles to perform the command
async def kickplayer(inter: disnake.ApplicationCommandInteraction, user: Users):
    with Client('<Server IP>', <RCON Port>, passwd='<AdminPassword>') as client:
        response = client.run(f'kickplayer {user}')
        await inter.response.send_message(f'Kicked player')

@kickplayer.error
async def kickplayer_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have the required role and cannot use this command.")


bot.run("<Bot-Token>")
