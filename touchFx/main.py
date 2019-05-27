import os
os.system("pd -nogui /home/pi/touchFx/effects.pd &")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from threading import *
import OSC
import math

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
oscServerHub.addMsgHandler('/quit',printingHandler)


	
##############################
#
# initialisation des variables globales
#
##############################

clip = 0
fx1act = 0
fx2act = 0
volAct = 0
	
##############################
#
# initialisation des serveur et client osc
#
##############################	
	
pd = ("localhost", 5000)
client = OSC.OSCClient()
client.connect( pd )

receiveAdress = '127.0.0.1',5001
oscServer = OSC.ThreadingOSCServer(receiveAdress)
oscServer.addDefaultHandlers()

client.sendto( OSC.OSCMessage("/echo", 1 ),pd )


def oscSendReverb(reverb):
	client.sendto(OSC.OSCMessage("/reverb", reverb), pd)
	return()
	
def oscSendDisto(disto):
	client.sendto(OSC.OSCMessage("/disto", disto), pd)
	return()
	
def oscSendFreq(freq):
	client.sendto(OSC.OSCMessage("/freq", freq), pd)
	return()

def oscSendLfo(lfo):
	client.sendto(OSC.OSCMessage("/lfo", lfo), pd)
	return()

def oscSendGain(gain):
	client.sendto(OSC.OSCMessage("/gain", gain), pd)
	return()

def printingHandler(addr, tags, stuff, source):
	global clip
	if addr=='/clip':
		clip = stuff[0]
oscServer.addMsgHandler('/clip',printingHandler)


##############################
#
# application kivy
#
##############################

class Fond(Widget):
	pass
	
class FxWidget(Widget):
	reverb = ObjectProperty(0)
	disto = ObjectProperty(0)
	freq = ObjectProperty(0)
	lfo = ObjectProperty(0)
	gain = ObjectProperty(0)
	gainNorm = ObjectProperty(0)
		
	def on_touch_up(self, touch):
		pass
		
	def on_touch_down(self, touch):
		if touch.y < 410:
			if touch.y > 30:
				if touch.x < 370:
					if touch.x>30:
						self.disto = (touch.x-30)/340
						self.reverb = (touch.y-30)/370
						oscSendDisto((touch.x-30)/340)
						oscSendReverb((touch.y-30)/370)
				elif touch.x > 430:
					if touch.x < 770:
						self.freq = (touch.x-430)/340
						self.lfo = (touch.y-30)/370
						oscSendFreq((touch.x-430)/340)
						oscSendLfo((touch.y-30)/370)
		elif touch.y > 440:
			if touch.x > 115:
				if touch.x <770:
					self.gainNorm = (touch.x-115)/655
					self.gain = int(math.exp(2*self.gainNorm)-1)

	def on_touch_move(self, touch):
		if touch.y < 440:
			if touch.x < 400:
				self.disto = min(max((touch.x-30)/340,0),1)
				self.reverb = min(max((touch.y-30)/370,0),1)
				oscSendDisto(min(max((touch.x-30)/340,0),1))
				oscSendReverb(min(max((touch.y-30)/370,0),1))
			elif touch.x > 400:
				self.freq = min(max((touch.x-430)/340,0),1)
				self.lfo = min(max((touch.y-30)/370,0),1)
				oscSendFreq(min(max((touch.x-430)/340,0),1))
				oscSendLfo(min(max((touch.y-30)/370,0),1))
		elif touch.y > 440:
			if touch.x > 115 and touch.x <770:
				self.gainNorm = (touch.x-115)/655
				self.gain = str(int(math.exp(2*self.gainNorm)-1))
				oscSendGain(self.gainNorm)		
					
	def update(self, dt):
		global clip
		pass
		image = self.ids.clipImage
		if clip==0:
			image.source = "clip.png"
		if clip==1:
			image.source = "clipclip.png"
		if quitter == 1:
			FxApp.get_running_app().stop()
		
class FxApp(App):
	def build(self):
		fx = FxWidget()
		Clock.schedule_interval(fx.update, 1.0/60.0)
		return fx
	def on_stop(self):
		oscServer.close()
		client.sendto( OSC.OSCMessage("/close", 1 ),pd )
		client.sendto(OSC.OSCMessage("/echo", 0), hub)
		oscServerHub.close()
		os.system("pkill pd")


##############################
#
# lancement des thread osc et kivy
#
##############################

osc = Thread(target=oscServer.serve_forever)
oscHub =  Thread(target=oscServerHub.serve_forever)


if __name__ == '__main__':
	osc.start()
	oscHub.start()
	FxApp().run()

