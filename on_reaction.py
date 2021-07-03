from replit import db
import jsonpickle
import constants


async def manage_reactions(client, payload):
    # If the message refers to one to start a game
    if str(payload.message_id) in db.keys():
        game = jsonpickle.decode(db[str(payload.message_id)])

        if not game.game_started:
            game.players = []

            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

            # Adds to the game all the users who added a reaction to the message
            for reaction in message.reactions:
                if reaction.emoji == constants.reaction_join:
                    async for user in reaction.users():
                        #if user != client.user:
                        game.players.append(user.mention)

            nb_reactions_ready = 0

            # Remove the ready status from all users who aren't players
            for reaction in message.reactions:
                if reaction.emoji == constants.reaction_ready:
                    async for user in reaction.users():
                        if user != client.user and not user.mention in game.players:
                            await message.remove_reaction(
                                    constants.reaction_ready, user)
                        else:
                          nb_reactions_ready += 1

            print(nb_reactions_ready)

            # If all players are ready and there are at least 4 and max 8, the game starts
            if len(game.players) > 4 and len(game.players) < 10 and len(game.players) == nb_reactions_ready:
              await message.channel.send("start_game()")

            # Edit the message
            await message.edit(content=constants.new_game_template.format(
                game.creator, ',\n'.join(game.players)))

        db[str(payload.message_id)] = jsonpickle.encode(game)


async def on_reaction_added(client, payload):
    await manage_reactions(client, payload)


async def on_reaction_removed(client, payload):
    await manage_reactions(client, payload)
