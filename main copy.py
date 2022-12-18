import discord
import os
from dotenv import load_dotenv
import AI.ai_chatbot as brain
import Functions.database_functions as database_function
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot online');

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = brain.predict_word(message.content)

    if(text == 'Hate Speech Detected'):
        response = database_function.update_database(str(message.guild.id), str(message.author.id))
    
        if(response == 1): 
            #ban user
            await message.channel.send("User banned");
        elif(response == 2):
            #kick user
            await message.channel.send("User kicked");


        print("========================================")
        print("Response: " + str(response))
        print("Total Warnings: " + str(database_function.get_total_warnings(str(message.guild.id), str(message.author.id))))
        print("Total Kicked: " + str(database_function.get_total_kicked(str(message.guild.id), str(message.author.id))))

load_dotenv()
client.run(os.getenv('TOKEN'))

