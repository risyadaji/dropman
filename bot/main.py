import discord
import time
import os

from formatter import genMessageFormat
from droplets import Droplet

from dotenv import load_dotenv

load_dotenv()
DO_PROJECT_TOKEN = os.getenv('DO_PROJECT_TOKEN')
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

client = discord.Client()
project = Droplet("Aji's Droplets", DO_PROJECT_TOKEN)

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=":dropman:"))
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith(':dropman:'):
    splitted = message.content.split(" ")
    
    if len(splitted) == 1:
      greetingFormat = '''
        **Droplets Manager is here!**
        > Here are the list that you can give me and order to do!
        > `droplets` to get all droplets based on your registered token
        > `action {type} {id}` set droplets active status either to `on` or `off` with defined `id`'''

      await message.channel.send(greetingFormat)

    else:
      command = splitted[1]
      params = splitted[2:]

      # List command.
      if command == "droplets":
        data = project.getDroplets() 
        for d in data:
          await message.channel.send(genMessageFormat("getlist", d))

      # Action 'on' droplet command.
      elif command == "action" and (params[0] == "on" or params[0] == "off"):
        dropletId = params[1]
        toggleType = "power_" + params[0]

        lastDroplet = project.getDetailDroplet(dropletId)
        action = project.toggleDropletStatus(dropletId, toggleType)
        await message.channel.send(genMessageFormat("toggle", action))

        timeout = time.time() + 20
        updatedDroplet = project.getDetailDroplet(dropletId)
        while lastDroplet['status'] == updatedDroplet['status'] and time.time() < timeout:
          time.sleep(2)
          updatedDroplet = project.getDetailDroplet(dropletId)

        await message.channel.send(genMessageFormat("getlist", updatedDroplet))

      else:
        await message.channel.send('> Invalid command')
   
client.run(DISCORD_TOKEN)
  
  
