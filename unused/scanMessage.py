from collections import deque  
from googleapiclient import discovery
from discord.ext import commands
import discord
import time
import json
import os

# Unused code

intents = discord.Intents.default()
intents.members = True


client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=os.getenv('APIKEY'),
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)


class ScanMessage(commands.Cog):



    def __init__(self, client):
        self.client = client

    def get_karma(self, client, message):
        with open('karma.json', 'r') as f:
            karma = json.load(f)


        return karma[str(message.author.id)]

    # @commands.Cog.listener()
    # async def on_guild_join(self, guild):
    #     for user in guild.members:
    #         with open('karma.json', 'r') as f:
    #             karma = json.load(f)

    #         if user.id not in karma:
    #             karma[str(user.id)] = 1
    #         with open('karma.json', 'w') as f:
    #             json.dump(karma, f, indent=4)    



    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     with open('karma.json', 'r') as f:
    #         karma = json.load(f)



    #     if member.id not in karma:
    #         karma[str(member.id)] = 1

    #     with open('karma.json', 'w') as f:
    #         json.dump(karma, f, indent=4)


    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print("[INFO] Module ready: Chat Scanner")

    # last_users = deque([])

    # @commands.Cog.listener()
    # async def on_message(self, message):

    #     if message.content:
            
    #         analyze_request = {
    #             'comment': { 'text': message.content },
    #             'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}}
    #     }   

    #         response = client.comments().analyze(body=analyze_request).execute()
    #         toxicity = float((json.dumps(
    #             response["attributeScores"]["TOXICITY"]["spanScores"][0]["score"]["value"])
    #             ))

    #         severe_toxicity = float((json.dumps(
    #             response["attributeScores"]["SEVERE_TOXICITY"]["spanScores"][0]["score"]["value"], indent=4)
    #             ))

    #         identity_attack = float((json.dumps(
    #             response["attributeScores"]["IDENTITY_ATTACK"]["spanScores"][0]["score"]["value"], indent=4)
    #             ))
    #         insult = float((json.dumps(
    #             response["attributeScores"]["INSULT"]["spanScores"][0]["score"]["value"], indent=4)
    #             ))


    #         with open('karma.json', 'r') as f:
    #             karma = json.load(f)


    #         if toxicity < 0.3:
    #             karma[str(message.author.id)] += 0.1
    #             if toxicity < 0.2:
    #                 karma[str(message.author.id)] += 0.2
    #                 if toxicity < 0.1:
    #                     karma[str(message.author.id)] += 0.3
    #         elif toxicity > 0.4:
    #             karma[str(message.author.id)] -= 0.1
    #             if toxicity > 0.55:
    #                 karma[str(message.author.id)] -= 0.2
    #                 if toxicity > 0.9:
    #                     karma[str(message.author.id)] -= 1
    #         with open('karma.json', 'w') as f:
    #             json.dump(karma, f, indent=4)

    #         time.sleep(2)




def setup(client):
    client.add_cog(ScanMessage(client))
