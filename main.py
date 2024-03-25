import disnake
from rcon.source import Client
from disnake.ext import commands
from enum import Enum

####
# Define your users - replace with actual player SteamIDs
class Users(str, Enum):
    Player1 = 'SteamID1'
    Player2 = 'SteamID2'
    Player3 = 'SteamID3'

# Server configurations
servers = [
    {'Name': 'Server Name', 'IP': '127.0.0.1', 'RCONPort': 32331, 'Password': 'AdminPassword'},
    {'Name': 'Genesis 2', 'IP': '10.0.0.188', 'RCONPort': 32330, 'Password': '6e7vHguYVWH50k9tc'}, #Example, IP is set to MultiHome= in startup command (Can also be remote with port forwarding)
    # Add or remove more servers as necessary
]

# Replace 'between the quotes' with your bot's actual token
Token = 'bot-token'

# Time to wait for a server response, values below 1 may raise false-negatives
timeout = 2.5
####

bot = commands.Bot(command_prefix=disnake.ext.commands.when_mentioned)

@bot.slash_command(description="Kicks a player from all ARK servers where they are present")
#@commands.has_role(0000000000000000)  # Uncomment and replace with your admin role ID
async def kickplayer(inter: disnake.ApplicationCommandInteraction, user: Users):
    await inter.response.defer(ephemeral=False)

    for server in servers:
        server_name = server['Name']
        try:
            with Client(server['IP'], server['RCONPort'], passwd=server['Password'], timeout=1.5) as client:
                response = client.run(f'kickplayer {user}')
                print(f'{server_name} - {response}')
        except Exception as e:
            error_type = type(e).__name__
            print(f"Exception: {error_type} - {e}")

    print("Kicked player")
    await inter.edit_original_message(content=f'Kicked player across all servers.')

@kickplayer.error
async def kickplayer_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have the required role and cannot use this command.")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")

@bot.slash_command(description="Sends bot latency")
async def ping(inter: disnake.ApplicationCommandInteraction):
    await inter.response.send_message(f'{round(bot.latency * 1000)}ms')

@bot.slash_command(description="Lists connected players across all servers")
async def players(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer(ephemeral=False)

    # Construct an initial message with all servers listed as pending.
    initial_response = "\n".join([f"? {server['Name']}: Pending..." for server in servers])
    initial_response_with_formatting = f"```diff\n{initial_response}\n```"
    await inter.edit_original_message(content=initial_response_with_formatting)

    # A dictionary to keep track of the responses for each server.
    server_responses = {server['Name']: f"? {server['Name']}: Pending..." for server in servers}

    for server in servers:
        server_name = server['Name']
        try:
            with Client(server['IP'], server['RCONPort'], passwd=server['Password'], timeout=timeout) as client:
                raw_response = client.run('listplayers')
                # Check if the server response indicates no players are connected.
                if "No Players Connected" in raw_response:
                    formatted_response = "No Players Connected"
                else:
                    # Process the response to format it according to your requirements.
                    players_list = [
                        line.split('. ')[1].split(',')[0].strip() 
                        for line in raw_response.splitlines() 
                        if '. ' in line and ', ' in line.split('. ')[1]  # Ensuring the line has the expected format
                    ]
                    formatted_response = '\n'.join(players_list) if players_list else "No Players Connected"
                
                server_responses[server_name] = f'+ {server_name}:\n>> {formatted_response}\n'
        except Exception as e:
            error_type = type(e).__name__
            server_responses[server_name] = f'- {server_name} ({error_type})\n'
            print(f"Exception: {error_type} - {e}")
        
        # Construct the update message with the latest responses.
        update_message = "\n".join(server_responses.values())
        update_message_with_formatting = f"```diff\n{update_message}\n```"
        await inter.edit_original_message(content=update_message_with_formatting)



bot.run(Token)
