from collections import defaultdict
from typing import Dict, List

import discord
from discord import Member
from discord.channel import TextChannel
from discord.guild import Guild
from discord.role import Role
from discord.user import User
from discord.message import Message
from discord.embeds import Embed

import classes


client = discord.Client()
queues: Dict[str, List[Member]] = defaultdict(list)


def get_all_classes(guild: Guild) -> List[str]:
    roles: List[Role] = guild.roles
    r: Role
    return [r.name[6:] for r in roles if r.name.startswith('Class-')]


async def showclasses(user: Member, channel: TextChannel) -> None:
    out = user.mention + " List of classes:\n"
    out += "\n".join(get_all_classes(channel.guild))
    await channel.send(out)


async def joinqueue(user: Member, channel: TextChannel, cls: str) -> None:
    if cls not in get_all_classes(channel.guild):
        await channel.send(user.mention + ' Section {} does not exist.'.format(cls))
        return

    if user in queues[cls]:
        queues[cls].remove(user)
        await channel.send(user.mention + ' has left the {} queue.'.format(cls))
    else:
        queues[cls].append(user)
        await channel.send(user.mention + ' has joined the {} queue.'.format(cls))


async def showqueue(channel):
    for i in range(len(queue)):
        await channel.send(queue[i])


@classes.check_admin
async def ready(mentor: Member, channel, cls) -> None:
    student: Member = queues[cls].pop(0)
    await channel.send(mentor.mention + " is ready for " + student.mention + ".")


async def help(channel):
    embedVar = Embed(title="Help!", description="Possible commands:", color=0xf76902)
    embedVar.add_field(name="$joinqueue <class>", value="Add yourself to an existing queue.", inline=False)
    embedVar.add_field(name="$showqueue <class>", value="Show the people currently in queue.", inline=False)
    embedVar.add_field(name="$showclasses", value= "Lists all classes.", inline=False)
    embedVar.add_field(name="$ready (admin only)", value="Move to the next student in the queue.", inline=False)
    embedVar.add_field(name="$makeclass <name> (admin only)", value="Create a class.", inline=False)
    embedVar.add_field(name="$deleteclass <name> (admin only)", value="Deletes a class.", inline=False)
    embedVar.add_field(name="$clear <class> (admin only)", value="Clears the queue of the specified class.", inline=False)
    await channel.send(embed=embedVar)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@classes.check_admin
async def clear(caller, channel, cls):
    queues[cls] = list()
    await channel.send(caller + " has cleared the queue for " + cls + ".")

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    if message.content.startswith('$'):
        tokens: List[str] = message.content[1:].split(' ')
        if tokens[0] == 'joinqueue':
            await joinqueue(message.author, message.channel, tokens[1])
        elif tokens[0] == 'showclasses':
            await showclasses(message.author, message.channel)
        elif tokens[0] == 'ready':
            await ready(message.author, message.channel, tokens[1])
        elif tokens[0] == 'showqueue':
            await showqueue(message.channel)
        elif tokens[0] == 'help':
            await help(message.channel)
        elif tokens[0] == 'makeclass':
            await classes.makeclass(message.author, message.channel, tokens[1])
        elif tokens[0] == 'deleteclass':
            await classes.deleteclass(message.author, message.channel, tokens[1])
        elif tokens[0] == 'clear':
            await clear(message.author, message.channel, tokens[1])
        else:
            await message.channel.send("Invalid command. Type $help if you need somebody.")


client.run('NzU5NDU0ODE0NTUxMTQ2NTA2.X29vaQ.MuNF7XmF8mefy-_WzxB4vUYbAUM')
