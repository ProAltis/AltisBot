import discord
import asyncio
import config
import time
import traceback
import json
import urllib.request
import requests

class InvasionHandler():
    def __init__(self, client):
        self.client = client
        
    async def tracker(self):
        await self.client.wait_until_ready()
        messagelive = False
        while True == True:
            data = urllib.request.urlopen('https://www.projectaltis.com/api/invasion').read()
            invdata = json.loads(data)

            #Setting vars for use later
            district_name = ""
            invasion_cog = ""
            invasion_counter = ""

            for district in invdata['districts']: #Loops through the districts on the API
            	districtvalues = district.values() #Gets the values from the district.

            	#Getting district name, might be used later
            	for apikey in district:
            		districtname = apikey

            	#Starting invasion check
            	for valueloop in districtvalues:
            		if type(valueloop['invasion']) is dict: #Checking if district has a invasion
            			disval = valueloop['invasion'] #Less typing
            			district_name = district_name + "{}\n".format(districtname)
            			invasion_cog = invasion_cog + "{}\n".format(disval['cog'])
            			invasion_counter = invasion_counter + "{}/{} - {} Min left\n".format(disval['defeated'], disval['size'], disval['left'])
            		else: #If there is no invasion
            			pass #Ignore this district
            invasion_tracker_embed = discord.Embed(
            title="Invasion Tracker",
            type='rich',
            description="Updated every 5 seconds",
            colour=discord.Colour.green()
            )
            invasion_tracker_embed.add_field(name='District', value=district_name)
            invasion_tracker_embed.add_field(name='Cog', value=invasion_cog)
            invasion_tracker_embed.add_field(name='Status', value=invasion_counter)
            if messagelive == False:
                message = await self.client.send_message(discord.Object(id=387263295708725258), embed=invasion_tracker_embed)
                message
                messagelive = True
            elif messagelive == True:
                await self.client.edit_message(message, embed=invasion_tracker_embed)
            await asyncio.sleep(5)


    async def statustracker(self):
        await self.client.wait_until_ready()
        messagelive = False
        while True:
            embed = discord.Embed(
                title='Project Altis Status',
                type='rich',
                description='Statuses. Main Game is manually updated while the rest are checked every 5 minutes.',
                url='https://status.projectalt.is',
                colour=discord.Colour.green()
            )
            req = requests.get("https://status.projectalt.is/api/v1/components")

            # 1 = operational
            # 2 = performance
            # 3 = partial outage
            # 4 = major outage
            worst_status = 1
            try:
                jsn = json.loads(req.text)
                for dta in jsn["data"]:
                    if dta["status"] > worst_status:
                        worst_status = dta["status"]
                    embed.add_field(name=dta["name"], value=dta["status_name"])
            except:
                print("Cachet API is dying with code " + str(req.status_code) + ": " + req.text)
                return
            # Set color appropriately based on the worst status
            embed.colour = {
                1: discord.Colour.green(),
                2: discord.Colour.blue(),
                3: discord.Colour.gold(),
                4: discord.Colour.dark_red()
            }[worst_status]
            if messagelive == False:
                statusmessage = await self.client.send_message(discord.Object(id=387263295708725258), embed=embed)
                statusmessage
                messagelive = True
            elif messagelive == True:
                await self.client.edit_message(statusmessage, embed=embed)
            await asyncio.sleep(120)