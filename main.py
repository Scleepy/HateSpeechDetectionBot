import discord
import os
from dotenv import load_dotenv
import AI.LSTM_Model as brain
import Functions.database_functions as database_function
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot online');

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # guild = client.get_guild(message.guild.id)
    # member = guild.get_member(message.author.id)
    
    probability = brain.predict_word(message.content)
    #await message.channel.send(f'{member.mention}: probability is {probability * 100}%')

    if(probability > 0.95):
        response = database_function.update_database(str(message.guild.id), str(message.author.id))

        guild = client.get_guild(message.guild.id)
        member = guild.get_member(message.author.id)

        total_warnings = database_function.get_total_warnings(str(message.guild.id), str(message.author.id))
        total_kicked = database_function.get_total_kicked(str(message.guild.id), str(message.author.id))

        if(response == 1): 
            await message.channel.send(f'{member.mention} banned!')
            try:
                await member.ban(reason='User exceeded warning limit')
            except:
                print('User has higher privileges')

        elif(response == 2):
            await message.channel.send(f'{member.mention} kicked!')
            try:
                await member.kick(reason='User exceeded warning limit')
            except:
                print('User has higher privileges')
        
        else:
            await message.channel.send(f'{member.mention} Watch your words!')
            await message.channel.send(f'You have been warned {total_warnings} times and kicked {total_kicked} times!')
            await message.channel.send(f'You have {3 - total_warnings} warnings left!')

        print('========================================')
        print(f'Member: {member.name}')
        print(f'Response: {str(response)}')
        print(f'Total Warnings: {str(total_warnings)}')
        print(f'Total Kicked: {str(total_kicked)}')

load_dotenv()
client.run(os.getenv('TOKEN'))