import discord
from discord.ext import commands
import asyncio
import requests
import tplink_smartplug

Client = discord.Client()
client = commands.Bot(command_prefix = "!")
#live
#channel = discord.Object(id='') #Your personalized discord channel ID.
#BOT_TOKEN = ''

#testing:
channel = discord.Object(id='')
BOT_TOKEN = ''
IP_ONE = '192.168.1.216'
#IP_TWO = '192.168.1.171'

#Your pool must have an API - this is the base API address.
URL = "http://xsg.pool.sexy/api2/accounts/"
WALLET = "s1ZPk5Tij8NgkTknSAS9tks4CiTPtnwcTjp"
API_ADDRESS = URL + WALLET # change to match your pool API address.
NUM_WORKERS = 2 #Number of workers you should have up.

async def api_check():

    await client.wait_until_ready()


    #LOOP while the bot is running
    while not client.is_closed:
        workerStatus = getAPIdata()
        if workerStatus:
            await client.send_message(channel, "!!!!!!! WORKER DOWN !!!!!!!")
            print("Attempting to turn off the plugin")
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
        print("api check performed")
        await asyncio.sleep(300)  #rest for 5 minutes. POOL API MAY NOT LIKE CHECKING MORE OFTEN.



@client.event
async def on_ready():
    print("Mine-BOT IS RUNNING!")
    #
    # start logging /primarily for adding new coins or exchanges
    #   from requests !add
@client.event
async def on_message(message):
    msg = message.content.lower()
    if msg.startswith('?'):
        check = sysCheck()
        await client.send_message(channel, check)
    #Add further commands here "payments", etc
def sysCheck():

    status = requests.get(API_ADDRESS)
    if status.status_code == 200:
        stats = status.json()
        pymnt = str(stats["stats"]["paid"])[:-8]
        fullmsg = "Workers: " + str(stats["workersOnline"]) + "\n" + "Total Hashrate: " + str(stats["currentHashrate"]) + "\n" + "Paid: " + str(pymnt)
        return fullmsg

    return "Sorry fool, got nothing."

def getAPIdata():

    status = requests.get(API_ADDRESS)
    if status.status_code == 200:
        stats = status.json()
        if stats["workersOnline"] < NUM_WORKERS:
            return True
        elif stats["workersOnline"] == NUM_WORKERS:
            return False

client.loop.create_task(api_check())
client.run(BOT_TOKEN)