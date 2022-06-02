import discord
from discord.ext import commands
from datetime import datetime
import requests
import os
import aiohttp
import asyncio

client = commands.Bot(command_prefix='.')


# ONREADY
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# HELP COMMAND
# DISPLAY ALL THE COMMANDS
# REPLY IN SAME CHANNEL
@client.command(name='helpMe')
async def my_help(ctx):
    help_message = discord.Embed(
        title="**CPMC Discord Bot :robot:**",
        description='\n :loudspeaker:** Commands: ** \n\n :trophy:**.contests :** for upcomming contests \n\n :person_bouncing_ball:**.cf <username> :** for codeforces info of handle\n\n:person_bouncing_ball:**.lc <username> :** for leetcode info of handle \n\n **Thank you for using my services :smiley:**',
        color=0xFFA500
    )
    await ctx.reply(embed=help_message)


# CONTESTS COMMAND
# GET ALL CONTESTS
# REPLY IN SAME CHANNEL
URL_codeforces = "https://kontests.net/api/v1/codeforces"
URL_codechef = "https://kontests.net/api/v1/code_chef"
URL_leetcode = "https://kontests.net/api/v1/leet_code"

# sending get request and saving the response as response object
request_codeforces = requests.get(url=URL_codeforces)
request_codechef = requests.get(url=URL_codechef)
request_leetcode = requests.get(url=URL_leetcode)

# extracting data in json format
data_codeforces = request_codeforces.json()
data_codechef = request_codechef.json()
data_leetcode = request_leetcode.json()


def destructure_codeforces_leetcode(contest):
    date = contest['start_time'].split('T')[0]
    time = contest['start_time'].split('T')[1]
    return [contest['name'],
            str(date.split('-')[2] + "/" + date.split('-')[1] + "/" + date.split('-')[0] + " at " + str(
                int(time[0:2:1]) + 6) + ":05")]


def destructure_codechef(contest):
    date = contest['start_time'].split(' ')[0]
    time = contest['start_time'].split(' ')[1]
    return [contest['name'], str(
        date.split('-')[2] + "/" + date.split('-')[1] + "/" + date.split('-')[0] + " at " + str(
            int(time[0:2:1]) + 6) + ":00")]


codeforces_display_list = list(
    map(destructure_codeforces_leetcode, data_codeforces))

codechef_display_list = list(map(destructure_codechef, data_codechef))
codechef_display_list.reverse()

leetcode_display_list = list(
    map(destructure_codeforces_leetcode, data_leetcode))
leetcode_display_list.reverse()

display_list = codeforces_display_list[0:2:] + \
               codechef_display_list[0:2:] + leetcode_display_list[0:2:]


def display(display_list):
    dis = ''
    for contest in display_list:
        dis = dis + \
              f':trophy:  **Name**: {contest[0]}\n\n \t :clock8:  **Date**: {contest[1]}\n\n\n'
    dis+= '**Thank you for using my services :smiley:**\n\n'
    m = discord.Embed(
        title='\n**Upcoming Contests:**\n\n',
        description=dis,
        color=discord.Colour.blue()
    )
    return m


@client.command(name='contests')
async def contest(ctx):
    await ctx.reply(embed=display(display_list))


# CF COMMAND FOR CODEFORCES
# GET USERINFO
# REPLY IN DM
@client.command(name='cf')
async def userInfo(ctx, name):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://codeforces.com/api/user.info?handles={}'.format(name)) as response:
            data = await response.json()
            # print(data)
            if 'result' in data:
                data = data['result'][0]
                #         print('data', data)
                rating = data['rating'] if 'rating' in data else '\t'
                ft = data['firstName'] if 'firstName' in data else '\t'
                lt = data['lastName'] if 'lastName' in data else '\t'
                cntry = data['country'] if 'country' in data else '\t'
                rank = data['rank'] if 'rank' in data else '\t'
                maxrt = data['maxRating'] if 'maxRating' in data else '\t'
                m = discord.Embed(
                    title='this is your info',
                    description=f'**Request for** : \t{name}\n\n**Firstname :** \t{ft}\n\n**Lastname :** \t{lt}\n\n**Last Rating :** \t{rating}\n\n**country :** \t{cntry}\n\n**Rank :** \t{rank}\n\n**Max Rating :** \t{maxrt}\n\n**Thank you for using my services :smiley:**\n\n',
                    color=discord.Colour.red())
                await ctx.message.author.send(embed=m)
                await ctx.reply('**Info was successfully sent to you!!**')
            else:
                await ctx.reply('**404 Player Not found**')

# LC COMMAND FOR LEETCODE
@client.command(name='lc')
async def userInfo(ctx, name):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://competitive-coding-api.herokuapp.com/api/leetcode/{}'.format(name)) as response:
            data = await response.json()
            if 'ranking' in data:
                ranking = data['ranking'] if 'ranking' in data else '\t'
                problems = data['total_problems_solved'] if 'total_problems_solved' in data else '\t'
                points = data['contribution_points'] if 'contribution_points' in data else '\t'
                rep = data['reputation'] if 'reputation' in data else '\t'
                m = discord.Embed(
                    title='this is your info',
                    description=f'**Request for** : \t{name}\n\n**Rank :** \t{ranking}\n\n**Problems Solved :** \t{problems}\n\n**Total Points :** \t{points}\n\n**Reputation :** \t{rep}\n\n**Thank you for using my services :smiley:**\n\n',
                    color=discord.Colour.white())
                await ctx.message.author.send(embed=m)
                await ctx.reply('**Info was successfully sent to you!!**')
            else:
                await ctx.reply('**404 Player Not found**')


client.run(os.environ['DISCORD_TOKEN'])
