from replit import db
from time_bomb_class import *
import jsonpickle

new_game_template = "{0} a lancé une nouvelle partie. Cliquez sur 🇯 pour la rejoindre."


async def on_message_detected(client, message):
    if message.author == client.user:
        return

    # If the message is not send in the channel to create new games
    if message.channel.id != 857997333966487572:
        return

    # For now, the only possible command is to create a new game
    if message.content != "!newGame":
        return

    # A new game is requested, we show a message telling the name of the user who created it, and set a reaction to join the game
    msg = await message.channel.send(new_game_template.format(message.author.mention))
    await msg.add_reaction('🇯')

    tb = time_bomb()
    tb.id = str(msg.id)

    db[tb.id] = jsonpickle.encode(tb)
    print(jsonpickle.decode(db[tb.id]))
