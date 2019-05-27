import os

if __name__ == '__main__':
	os.system("csound /home/pi/csound/test.csd &")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, ListProperty

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
oscServerHub.addMsgHandler('/quit',printingHandler)


##############################
#
# initialisation des variables globales
#
##############################

midi = 0
envMod = 0

##############################
#
# initialisation des serveur et client osc
#
##############################	
	
csound = ("localhost", 5002)
client = OSC.OSCClient()
client.connect( csound )

receiveAdress = '127.0.0.1',5003
oscServer = OSC.ThreadingOSCServer(receiveAdress)
oscServer.addDefaultHandlers()

def oscSendVolume(volume):
	client.sendto(OSC.OSCMessage("/volume",volume), csound)
	print volume
	return()
	
def oscSendCutoff(cutoff):
	client.sendto(OSC.OSCMessage("/cutoff",cutoff*6000), csound)
	print cutoff
	return()
	
def oscSendResonnance(resonnance):
	client.sendto(OSC.OSCMessage("/resonnance",resonnance*0.79), csound)
	return()
	
def oscSendAttaque(attaque):
	client.sendto(OSC.OSCMessage("/attaque",attaque), csound)
	return()
	
def oscSendRelease(release):
	client.sendto(OSC.OSCMessage("/release",release), csound)
	return()
	
def oscSendEnvMod(envMod):
	client.sendto(OSC.OSCMessage("/envMod",envMod), csound)
	return()

def oscSendEffectMix(mix):
	client.sendto(OSC.OSCMessage("/mix",mix), csound)
	return()
	
def oscSendEffectRate(rate):
	client.sendto(OSC.OSCMessage("/rate",rate), csound)
	return()
		
def printingHandler(addr, tags, stuff, source):
	global midi
	if addr=='/midi':
		midi = stuff[0]

oscServer.addMsgHandler('/midi',printingHandler)


##############################
#
# application kivy
#
##############################

class SynthWidget(Widget):
	posVolume = ObjectProperty(35)
	posCutoff = ObjectProperty(35)
	posResonnance = ObjectProperty(35)
	posAttaque = ObjectProperty(35)
	posRelease = ObjectProperty(35)
	posEnvMod = ObjectProperty(35)
	posEffectMix = ObjectProperty(35)
	posEffectRate = ObjectProperty(35)
	color = ListProperty([0.5,0.5,0.5])

######################	
	def on_touch_up(self, touch):
		global envMod
		if touch.x>700:
			if touch.y<240:
				envMod = (envMod + 1) %2
				oscSendEnvMod(envMod)
				if envMod==1:
					self.ids.envMod.source="images/on.png"
				else:
					self.ids.envMod.source="images/off.png"
######################	
	def on_touch_down(self, touch):
		if touch.x<100:
			self.posVolume = max(min(touch.y-15,415),35)
			oscSendVolume(max(min((touch.y-50)/395,1),0))
		elif touch.x<200:
			self.posCutoff = max(min(touch.y-15,415),35)
			oscSendCutoff(max(min((touch.y-50)/395,1),0))
		elif touch.x<300:
			self.posResonnance = max(min(touch.y-15,415),35)
			oscSendResonnance(max(min((touch.y-50)/395,1),0))
		elif touch.x<400:	
			self.posAttaque = max(min(touch.y-15,415),35)
			oscSendAttaque(max(min((touch.y-50)/395,1),0))				
		elif touch.x<500:
			self.posRelease = max(min(touch.y-15,415),35)
			oscSendRelease(max(min((touch.y-50)/395,1),0))
		elif touch.x<600:
			self.posEffectMix = max(min(touch.y-15,415),35)
			oscSendEffectMix(max(min((touch.y-50)/395,1),0))
		elif touch.x<700:
			self.posEffectRate = max(min(touch.y-15,415),35)
			oscSendEffectRate(max(min((touch.y-50)/395,1),0))


##########################################	
	def on_touch_move(self, touch):
		if touch.x<100:
			self.posVolume = max(min(touch.y-15,415),35)
			oscSendVolume(max(min((touch.y-50)/395,1),0))
		elif touch.x<200:
			self.posCutoff = max(min(touch.y-15,415),35)
			oscSendCutoff(max(min((touch.y-50)/395,1),0))
		elif touch.x<300:
			self.posResonnance = max(min(touch.y-15,415),35)
			oscSendResonnance(max(min((touch.y-50)/395,1),0))
		elif touch.x<400:	
			self.posAttaque = max(min(touch.y-15,415),35)
			oscSendAttaque(max(min((touch.y-50)/395,1),0))				
		elif touch.x<500:
			self.posRelease = max(min(touch.y-15,415),35)
			oscSendRelease(max(min((touch.y-50)/395,1),0))
		elif touch.x<600:
			self.posEffectMix = max(min(touch.y-15,415),35)
			oscSendEffectMix(max(min((touch.y-50)/395,1),0))
		elif touch.x<700:
			self.posEffectRate = max(min(touch.y-15,415),35)
			oscSendEffectRate(max(min((touch.y-50)/395,1),0))
###############################		
	def update(self,dt):
		global midi
		if midi != 0:
			self.color = [0,1,0]
			midi = 0
		else:
			self.color = [0.5,0.5,0.5]
		if quitter == 1:
			SynthApp.get_running_app().stop()

class SynthApp(App):
	def build(self):
		synth = SynthWidget()
		Clock.schedule_interval(synth.update, 1.0/30.0)
		return synth
	def on_stop(self):
		oscServer.close()
		client.sendto( OSC.OSCMessage("/close", 1 ),csound )
		client.sendto(OSC.OSCMessage("/echo", 0), hub)
		oscServerHub.close()
		os.system("pkill csound")


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
	SynthApp().run()

