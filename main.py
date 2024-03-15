import discord
import webcolors
from discord import app_commands
from os import getenv
from re import match


class ColourMe(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)


intents = discord.Intents.default()
colour_me = ColourMe(intents=intents)


@colour_me.tree.command()
@app_commands.describe(colour='The colour you want your name. Can be a name or hex. E.g. "red", "blue", "#ff6464", "invis(ible)"')
async def colour(interaction: discord.Interaction, colour: str):
    '''Changes the colour of your discord name'''

    if colour.lower() in webcolors.CSS3_NAMES_TO_HEX:
        colour_hex = webcolors.name_to_hex(colour)[1:]
    elif match('^#[0-9a-f]{6}$', colour):
        colour_hex = colour[1:] # remove the '#'
    elif match('^[0-9a-f]{6}$', colour):
        colour_hex = colour
    elif match('(invis)|(invisible)', colour):
        colour_hex = '313338'
    else:
        await interaction.response.send_message('wtf was that??. Say something like "blue", "red" or "#ff00ff"')
        return

    # because discord doesn't allow pure black
    if colour_hex == '000000':
        colour_hex = '010101'
    
    discord_colour = discord.Color(int(colour_hex, 16))

    role_name = f'colour-{interaction.user.id}'
    for role in interaction.guild.roles:
        if role.name == role_name:
            await role.edit(colour=discord_colour)
            break
    else:  # else runs if for loop doesn't break. I.e. It doesn't find a role
        role = await interaction.guild.create_role(name=role_name, colour=discord_colour)
    
    if interaction.user not in role.members:
        await interaction.user.add_roles(role)
    
    await interaction.response.send_message('Done :3')


discord_token = getenv('discord_token')

if len(discord_token) < 20:
    print("Please provide a valid token to the discord_token environment variable")
    exit()

colour_me.run(discord_token)
