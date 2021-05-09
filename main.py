import discord
import os

from dotenv import load_dotenv
from droplets import Droplet

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
          msgFormat = '''
          > **{name}**
          > **ID**: {id}
          > **Memory**: {memory}
          > **Disk**: {disk}
          > **CPU**: {cpu}
          > **Status**: {status}
          '''.format(name=d['name'], id=d['id'], memory=d['memory'], disk=d['disk'], cpu=d['cpu'], status=d['status'])

          await message.channel.send(msgFormat)

      # Action 'on' droplet command.
      elif command == "action" and (params[0] == "on" or params[0] == "off"):
        dropletId = params[1]
        toggleType = "power_" + params[0]
        resp = project.toggleDropletStatus(dropletId, toggleType)

        msgFormat = '''
        > **Type**: {type}
        > **Status**: {status}
        > **Started At**: {startedAt}
        '''.format(type= resp['type'], status=resp['status'], startedAt=resp['startedAt'])

        await message.channel.send(msgFormat)

        # TODO ADD BACKGROUND TASK WHEN TOOGLING ACTION TO CALLBACK DROPLET STATUS

      else:
        await message.channel.send('> Invalid command')
   
client.run(DISCORD_TOKEN)
