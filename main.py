import discord
from discord.ext import commands
import asyncio
import requests
import tplink_smartplug

Client = discord.Client()
client = commands.Bot(command_prefix = "!")
#live
channel = discord.Object(id='') #Your personalized discord channel ID.
BOT_TOKEN = ''

IP_ONE = '192.168.1.100'
#IP_TWO = '192.168.1.101'

#Your pool must have an API - this is the base API address.
URL = "http://xsg.pool.sexy/api2/accounts/"
WALLET = "s1ZPk5Tij8NgkTknSAS9tks4CiTPtnwcTjp"
API_ADDRESS = URL + WALLET # change the format to match your pool API address.
#I only have two rigs, and only one freezes. So this is a simple check for me.
#   If more than one rig is the problem.  A rig class could be created.  Injecting the worker name, or
#    if you went the ping route, this would be easy as well.
NUM_WORKERS = 2 
 
async def api_check():

    await client.wait_until_ready()


    #LOOP while the bot is running
    while not client.is_closed:
        workerStatus = getAPIdata()
        if workerStatus:
            await client.send_message(channel, "!!!!!!! WORKER DOWN !!!!!!!")
            if tplink_smartplug.validIP(IP_ONE):  #Validates the IP address / may not be needed if you trust your ip up top.
                tplink_smartplug.setIP(IP_ONE)
                tplink_smartplug.sendCmd(b"{\"system\":{\"set_relay_state\":{\"state\":0}}}") #turn off - state = 0
            # TURN OFF PLUGIN TWO
            # if tplink_smartplug.validIP(IP_TWO):  #Validates the IP address
            #     tplink_smartplug.setIP(IP_TWO)
            #     tplink_smartplug.sendCmd(b"{\"system\":{\"set_relay_state\":{\"state\":0}}}") #turn off - state = 0

            await asyncio.sleep(10) #wait for 10 seconds and we'll turn the plugins back on.

            if tplink_smartplug.validIP(IP_ONE):  #Validates the IP address
                tplink_smartplug.setIP(IP_ONE)
                tplink_smartplug.sendCmd(b"{\"system\":{\"set_relay_state\":{\"state\":1}}}") #turn on - state = 1
            # TURN OFF PLUGIN TWO
            # if tplink_smartplug.validIP(IP_TWO):  #Validates the IP address
            #     tplink_smartplug.setIP(IP_TWO)
            #     tplink_smartplug.sendCmd(b"{\"system\":{\"set_relay_state\":{\"state\":1}}}") #turn on - state = 1
            await client.send_message(channel, "Power cycled. Check back in 5 minutes...")
        print("api check performed")
        await asyncio.sleep(300)  #rest for 5 minutes. POOL API MAY NOT LIKE CHECKING MORE OFTEN.

@client.event
async def on_ready():
    print("Mine-BOT IS RUNNING!")

@client.event
async def on_message(message):
    msg = message.content.lower()
    if msg.startswith('?'):
        check = sysCheck()
        await client.send_message(channel, check)
    #Add further commands here "payments", etc

#returns worker data from pool
def sysCheck():
    status = requests.get(API_ADDRESS)
    if status.status_code == 200:
        stats = status.json()
        pymnt = str(stats["stats"]["paid"])[:-8]
        fullmsg = "Workers: " + str(stats["workersOnline"]) + "\n" + "Total Hashrate: " + str(stats["currentHashrate"]) + "\n" + "Paid: " + str(pymnt)
        return fullmsg

    return "Sorry fool, got nothing."

#Pulls API data on your workers.  THIS WILL BE DIFFERENT BASED ON THE POOL.
def getAPIdata():
    status = requests.get(API_ADDRESS)
    if status.status_code == 200:
        stats = status.json()
        if stats["workersOnline"] < NUM_WORKERS:
            return True
        elif stats["workersOnline"] == NUM_WORKERS:
            return False

client.loop.create_task(api_check()) #makes the loop function run like a coroutine.
client.run(BOT_TOKEN)
