import discord
import webcolors
from discord import app_commands
from os import getenv


class ColourMe(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)


intents = discord.Intents.default()
colour_me = ColourMe(intents=intents)


@client.tree.command()
@app_commands.describe(
    colour='The colour you want your name. Can be a name or hex. E.g. "red", "blue", "#ff6464"'
)
async def colour(interaction: discord.Interaction, colour: str):
    '''Changes the colour of your discord name'''

    if colour.lower() in webcolors.CSS3_NAMES_TO_HEX:
        colour = webcolors.name_to_hex(colour)
    
    # because black is not allowed
    if colour == '#000000':
        colour = '#010101'

    try:
        colour = discord.Color(int(colour[1:], 16))
    except:
        await interaction.response.send_message('wtf was that??. Say something like "blue", "red" or "#ff00ff"')
        return

    role_name = f'colour-{interaction.user.id}'
    for role in interaction.guild.roles:
        if role.name == role_name:
            await role.edit(colour=colour)
            break
    else:  # if no role found
        role = await interaction.guild.create_role(name=role_name, colour=colour)
    
    if interaction.user not in role.members:
        await interaction.user.add_roles(role)
    
    await interaction.response.send_message("Done :3")


colour_me.run(getenv('discord_token'))
