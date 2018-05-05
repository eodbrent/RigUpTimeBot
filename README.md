# RigUpTimeBot

Main purpose is to increase the uptime of my mining rig.  I've had freezing issues that I cannot troubleshoot. The freezes required
a power cycle which I had to do VIA my phone and a smart plugin.  I found softScheck's TP-Link Smartplug reverse engineered article, and
the repo.  I then incorporated that into a discord bot.  I'm sure you could change the API check to a rig ping, but that was inconsistent
for me.

Simply change the wallet address and API address for your pool.  Add your smart plug IP address (LAN if you're running from a Raspberry Pi
on  your home network, or WAN address if you're running from a heroku type server).  Total JSON commands can be found at softScheck repo.
The on off states were sufficient for me.
