import os
from threading import *
import OSC


#############################
#
#	connection hub
#
#############################

hub = ("localhost", 4000)
client = OSC.OSCClient()
client.connect( hub )

client.sendto(OSC.OSCMessage("/echo", 1), hub)

hubAdress = '127.0.0.1',4001
oscServerHub = OSC.ThreadingOSCServer(hubAdress)
oscServerHub.addDefaultHandlers()

quitter = 0
def printingHandler(addr, tags, stuff, source):
	global quitter
	if addr=='/quit':
		quitter = stuff[0]
	if quitter == 1:
		client.sendto(OSC.OSCMessage("/echo", 0), hub)
		oscServerHub.close()
		os.system('pkill pd')
		quit()
oscServerHub.addMsgHandler('/quit',printingHandler)

#######################
#
# demarrage
#
#######################

oscHub =  Thread(target=oscServerHub.serve_forever)

if __name__ == '__main__':
	oscHub.start()
	os.system("pd -nogui /home/pi/fxGem/fxLite.pd &")
