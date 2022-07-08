import discord
from discord.ext import commands
import requests
import os
import aiohttp
import asyncio
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time, timedelta, date

client = commands.Bot(command_prefix=';')

# ONREADY


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# HELP COMMAND
# DISPLAY ALL THE COMMANDS
# REPLY IN SAME CHANNEL
@client.command(name='helpme')
async def my_help(ctx):
    help_message = discord.Embed(
        title="**CPMC Discord Bot :robot:**",
        description='\n :loudspeaker:** Commands: ** \n\n :trophy:  **;contests :** for upcomming contests \n\n :joystick:  **;rating <platform> <username> :** for rating info of handle \n\n\tplatform options: \n\n\t\t:chart_with_upwards_trend:  cf for codeforces \n\n\t\t:chart_with_upwards_trend:  cc for codechef \n\n\t\t:chart_with_upwards_trend:  lc for leetcode \n\n:joystick: **;graph <platform> <username>** \n\nplatform options: \n\n\t\t:chart_with_upwards_trend:  cf for codeforces \n\n\t\t:chart_with_upwards_trend:  cc for codechef\n\n:joystick:  **;rq <difficulty_level> :** for random leetcode question\n\n options for difficulty_level: \n\n :muscle: Easy \n\n :muscle: Medium \n\n :muscle: Hard \n\n :joystick:  **;rt <tag> :** for random codeforces questions with tag \n\n Options for tags: https://codeforces.com/blog/entry/14565 \n\n**Thank you for using my services :smiley:**',
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
                int(time[0:2:1]) + 6) + ":00")]


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
    codechef_display_list[2:4:] + leetcode_display_list[0:2:]


def display(display_list):
    dis = ''
    for contest in display_list:
        dis = dis + \
            f':trophy:  **Name**: {contest[0]}\n\n \t :clock8:  **Date**: {contest[1]}\n\n\n'
    dis += '**Thank you for using my services :smiley:**\n\n'
    message = discord.Embed(
        title='\n**Upcoming Contests:**\n\n',
        description=dis,
        color=discord.Colour.blue()
    )
    return message


@client.command(name='contests')
async def contest(ctx):
    await ctx.reply(embed=display(display_list))


@client.command(name='rating')
async def rating(ctx, platform, name):
    if platform == 'cf':
        async with aiohttp.ClientSession() as session:
            async with session.get('https://codeforces.com/api/user.info?handles={}'.format(name)) as response:
                data = await response.json()

                if 'result' in data:
                    data = data['result'][0]
                    rating = data['rating'] if 'rating' in data else '\t'
                    rank = data['rank'] if 'rank' in data else '\t'
                    maxrt = data['maxRating'] if 'maxRating' in data else '\t'
                    m = discord.Embed(
                        title='this is your info for codeforces',
                        description=f'**Request for** : \t{name}\n\n**Last Rating :** \t{rating}\n\n**Rank :** \t{rank}\n\n**Max Rating :** \t{maxrt}\n\n**Thank you for using my services :smiley:**\n\n',
                        color=discord.Colour.red())
                    await ctx.message.author.send(embed=m)
                    await ctx.reply('**Info was successfully sent to you!!**')
                else:
                    await ctx.reply('**400 Player Not found or contests not given**')
    elif platform == 'cc':
        async with aiohttp.ClientSession() as session:
            async with session.get('https://contest-details.herokuapp.com/api/codechef/{}'.format(name)) as response:
                data = await response.json()
                if 'div' in data:
                    ranking = data['country rank'] if 'country rank' in data else '\t'
                    problems = data['problem solved'] if 'problem solved' in data else '\t'
                    div = data['div'] if 'div' in data else '\t'
                    stars = data['stars'] if 'stars' in data else '\t'
                    maxRt = data['max rating'] if 'max rating' in data else '\t'
                    current = data['rating'] if 'rating' in data else '\t'
                    m = discord.Embed(
                        title='this is your info for codechef',
                        description=f'**Request for** : \t{name}\n\n**Rank :** \t{ranking}\n\n**Div :** \t{div}\n\n**Stars :** \t{stars}\n\n**Rating :** \t{current}\n\n**Max Rating :** \t{maxRt}\n\n**Problems Solved :** \t{problems}\n\n**Thank you for using my services :smiley:**\n\n',
                        color=discord.Colour.green())
                    await ctx.message.author.send(embed=m)
                    await ctx.reply('**Info was successfully sent to you!!**')
                else:
                    await ctx.reply('**400 Player Not found or contests not given**')
    elif platform == 'lc':
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    'https://competitive-coding-api.herokuapp.com/api/leetcode/{}'.format(name)) as response:
                data = await response.json()
                if 'ranking' in data:
                    ranking = data['ranking'] if 'ranking' in data else '\t'
                    problems = data['total_problems_solved'] if 'total_problems_solved' in data else '\t'
                    points = data['contribution_points'] if 'contribution_points' in data else '\t'
                    rep = data['reputation'] if 'reputation' in data else '\t'
                    m = discord.Embed(
                        title='this is your info for leetcode',
                        description=f'**Request for** : \t{name}\n\n**Rank :** \t{ranking}\n\n**Problems Solved :** \t{problems}\n\n**Total Points :** \t{points}\n\n**Reputation :** \t{rep}\n\n**Thank you for using my services :smiley:**\n\n',
                        color=0xffffff)
                    await ctx.message.author.send(embed=m)
                    await ctx.reply('**Info was successfully sent to you!!**')
                else:
                    await ctx.reply('**400 Player Not found or contests not given**')
    else:
        await ctx.reply('**Enter valid platform**')


# RANDOM QUESTION
# GET QUESTIONS FROM LEETCODE AND RETURN RANDOM QUESTION
# REPLY IN SAME CHANNEL
def get_questions(difficulty='medium'):
    URL_question = f'https://leetcode-api-1d31.herokuapp.com/api/questions/{difficulty}'
    raw_questions = requests.get(url=URL_question)
    question_data = raw_questions.json()['data']['questiions']
    random_index = random.randint(0, len(question_data))
    random_question = question_data[random_index]
    link = f"https://leetcode.com/problems/{random_question['titleSlug']}"
    message = discord.Embed(
        title="**Random Question**",
        description=f'\n\n**Difficulty: ** {random_question["difficulty"]} \n\n **Title: ** {random_question["title"]} \n\n **Link :** {link}',
        color=discord.Colour.green()
    )
    return message


@client.command(name='rq')
async def rand_question(ctx, difficulty='medium'):
    await ctx.reply(embed=get_questions(difficulty))


def get_question_tag(tag):
    URL_randtag = f'https://codeforces.com/api/problemset.problems?tags={tag}'
    raw_questions = requests.get(url=URL_randtag)
    if 'result' not in raw_questions.json():
        return discord.Embed(title='Tag not found')
    question_data = raw_questions.json()['result']['problems']
    random_index = random.randint(0, len(question_data))
    random_question = question_data[random_index]
    link = f"https://codeforces.com/problemset/problem/{random_question['contestId']}/{random_question['index']}"
    message = discord.Embed(
        title="**Random Codeforces Question**",
        description=f'\n\n**Difficulty: ** {random_question["index"]} \n\n **Title: ** {random_question["name"]} \n\n **Link :** {link}',
        color=discord.Colour.dark_blue()
    )
    return message


@client.command(name='rt')
async def rand_question_tag(ctx, tag):
    await ctx.reply(embed=get_question_tag(tag))


font = {'size': 7}


def filterRating(contest):
    return contest['newRating']


@client.command(name='graph')
async def graph_disp(ctx, platform, user):
    if platform == 'cc':
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://contest-details.herokuapp.com/api/codechef/{user}') as response:
                data = await response.json()
                if 'contests' in data:
                    x = np.arange(0, len(data['contests']))
                    y = data['contests']
                    plt.clf()
                    for i_x, i_y in zip(x, y):
                        plt.text(i_x, i_y, '{}'.format(i_y), fontdict=font)
                    plt.plot(x, y)
                    plt.xlabel("time period")
                    plt.ylabel("Rating")
                    plt.title("Codechef Rating")
                    plt.savefig(f"{user}.png")

                    file = discord.File(f'{user}.png', filename=f'{user}.png')
                    await ctx.message.author.send(file=file)
                    await ctx.reply('**Graph was successfully sent to you!!**')
                else:
                    await ctx.reply('**400 Player Not found or contests not given**')
    elif platform == 'cf':
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://codeforces.com/api/user.rating?handle={user}') as response:
                data = await response.json()
                if 'result' in data:
                    rating_list = list(map(filterRating, data['result']))
                    x = np.arange(0, len(rating_list))
                    y = rating_list
                    plt.clf()
                    for i_x, i_y in zip(x, y):
                        plt.text(i_x, i_y, '{}'.format(i_y), fontdict=font)
                    plt.plot(x, y)
                    plt.xlabel("time period")
                    plt.ylabel("Rating")
                    plt.title("Codeforces Rating")
                    plt.savefig(f"{user}.png")

                    file = discord.File(f'{user}.png', filename=f'{user}.png')
                    await ctx.message.author.send(file=file)
                    await ctx.reply('**Graph was successfully sent to you!!**')
                else:
                    await ctx.reply('**400 Player Not found or contests not given**')
client.run(os.environ['DISCORD_TOKEN'])
