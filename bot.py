import disnake
from rcon.source import Client
from disnake.ext import commands
from enum import Enum

class Users(str, Enum): 
    PlayerUsername = '112233445566' # Replace with each username, and the numbers with their SteamID
    PlayerUsername2 = '112233445567'
    PlayerUsername3 = '112233445568'

# Server configurations
servers = [
    {'Name': 'Server1', 'IP': '127.0.0.1', 'RCONPort': 32330, 'Password': 'AdminPassword1'}#, # If you have multiple servers, uncomment and expand as needed
    #{'Name': 'Server2', 'IP': '127.0.0.1', 'RCONPort': 32331, 'Password': 'AdminPassword2'} 
]

Token = 'BotToken' # Replace with the Discord Bot Token from the Developer Portal

bot = commands.InteractionBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")


@bot.slash_command(description="Lists connected ARK players")
async def players(inter):
    all_responses = []
    for server in servers:
        with Client(server['IP'], server['RCONPort'], server['Password']) as client:
            try:
                response = client.run('listplayers')
                all_responses.append(f'{server["Name"]}:\n{response}')
            except Exception as Err:
                all_responses.append(f'Error in {server["Name"]}:\n{Err}')
    
    await inter.response.send_message('\n\n'.join(all_responses))

@bot.slash_command(description="Kicks an ARK player from the server")
async def kickplayer(inter, user: Users):
    all_responses = []
    for server in servers:
        with Client(server['IP'], server['RCONPort'], server['Password']) as client:
            try:
                client.run(f'kickplayer {user}')
                all_responses.append(f'Kicked player from {server["Name"]}')
            except Exception as Err:
                all_responses.append(f'Error in {server["Name"]}:\n{Err}')
    
    await inter.response.send_message('\n\n'.join(all_responses))


@kickplayer.error
async def kickplayer_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have the required role and cannot use this command.")

@players.error
async def players_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have the required role and cannot use this command.")

bot.run(Token)
