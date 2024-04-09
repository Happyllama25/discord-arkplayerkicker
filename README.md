# discord-arkplayerkicker
Kicks players from an ARK server with a discord bot (Slash commands)

Very niche use, could be used for admin purposes (?) currently use it to kick a player who is very prone to crashes of their game client, if a client crashes, the player is still connected to the server, giving them the "Connection Failure: There is already a player with this account connected!" error.

**It can take ARK up to 8 minutes to time out a lost connection**, and in that time, they can be targeted by wild creatures in the server, as well as keep their area loaded, which could cause other issues like dinos attacking wild creatures and running away to get lost.

### Running:
`pip install -r requirements.txt`

`python main.py`

If you need help, open an issue, happy to help with configuration!

# TO-DO
- Player authentication/linking - so only linked players can kick themselves and not others
