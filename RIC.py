import discord
from discord.ext import commands
from datetime import datetime
import requests

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


URL = "https://codeforces.com/api/contest.list?gym=false"

# sending get request and saving the response as response object
r = requests.get(url=URL)

# extracting data in json format
data = r.json()

contests = data['result']


def upcoming(contest):
    if contest['phase'] == 'BEFORE':
        return True
    else:
        return False


def destructure(contest):
    return [contest['name'], datetime.fromtimestamp(contest['startTimeSeconds']).strftime("%A, %B %d, %Y %I:%M:%S")]


contest_list = list(filter(upcoming, contests))

display_list = list(map(destructure, contest_list))


def display(display_list):
    dis = '\n**Upcoming Contests:**\n\n'
    i = 1
    for contest in display_list:
        dis = dis + f'{i}) **Name**: {contest[0]}\n \t**Date**: {contest[1]}\n\n'
        i = i + 1
    return dis


@client.command(name='contests')
async def contest(ctx):
    await ctx.reply(display(display_list))


client.run('OTc4NzMxNjAwMzc0Mjg0MzIy.G4ygGK.DUuxYU1R6MpX-4Li6Ms38v6FOk7UlYHN0ouHMg')
