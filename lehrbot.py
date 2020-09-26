from typing import List

import discord
from discord import Member
from discord.user import User
from discord.message import Message


client = discord.Client()

queue = []


async def joinqueue(user: User, channel) -> None:
    if user in queue:
        queue.remove(user)
    else:
        queue.append(user)
    await channel.send(str(queue))


async def ready(mentor: Member, channel) -> None:
    student: Member = queue.pop(0)
    await channel.send(mentor.mention + " is ready for " + student.mention)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    if message.content.startswith('$'):
        tokens: List[str] = message.content[1:].split(' ')
        if tokens[0] == 'joinqueue':
            await joinqueue(message.author, message.channel)
        elif tokens[0] == 'ready':
            await ready(message.author, message.channel)
        await message.channel.send('Hello!')


client.run('NzU5NDU0ODE0NTUxMTQ2NTA2.X29vaQ.MuNF7XmF8mefy-_WzxB4vUYbAUM')
