from replit import db
from time_bomb_class import *
import jsonpickle
import constants


async def on_message_detected(client, message):
    if message.author == client.user:
        return

    # If the message is not send in the channel to create new games
    if message.channel.id != 857997333966487572:
        return

    if "!mockReaction" in message.content:
      await mockReaction(client, message)

    # For now, the only possible command is to create a new game
    if message.content != "!newGame":
        return

    # A new game is requested, we show a message telling the name of the user who created it, and set a reaction to join the game
    msg = await message.channel.send(
        constants.new_game_template.format(message.author.mention, ""))
    await msg.add_reaction(constants.reaction_join)
    await msg.add_reaction(constants.reaction_ready)

    tb = time_bomb()
    tb.id = str(msg.id)
    tb.creator = message.author.mention

    db[tb.id] = jsonpickle.encode(tb)
    print(jsonpickle.decode(db[tb.id]))
    
    print("json to save", jsonpickle.encode(tb))


#!mockReaction messageId reactionId userId
async def mockReaction(client, message):
  data = message.content.split()
  message_id = data[1]
  reaction_id = data[2]
  user_id = data[3]

  user = await client.fetch_user(user_id)

  message = await message.channel.fetch_message(message_id)
  

