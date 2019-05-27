import os
os.system("pd -nogui /home/pi/droneGenerator/drone.pd &")

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

tenu1 = 0
tenu2 = 0
tenu3 = 0
mode = 0
transpo = 0
transpo1depart = 0
transpo2depart= 0
transpo3depart =0

	
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

	
def oscSendNote(numKeyb,note):
	client.sendto(OSC.OSCMessage("/note"+str(numKeyb), note), pd)
	return()
	
def oscSendVol(vol):
	client.sendto(OSC.OSCMessage("/niveau", vol), pd)
	return()
	
def oscSendMode(mode):
	client.sendto(OSC.OSCMessage("/mode", mode), pd)
	return()

def oscSendIndice(indice):
	client.sendto(OSC.OSCMessage("/indice", indice), pd)
	return()

def oscSendEnv(env):
	client.sendto(OSC.OSCMessage("/env", env), pd)
	return()

##############################
#
# initialisation patch pure data
#
##############################

oscSendIndice(1)
oscSendVol(0.1)
oscSendMode(mode)


##############################
#
# application kivy
#
##############################



class DroneWidget(Widget):
	marqueur1 = ObjectProperty(-35)
	marqueur2 = ObjectProperty(-35)
	marqueur3 = ObjectProperty(-35)
	indice = ObjectProperty(1)
	volume = ObjectProperty(1)
	masque = ObjectProperty(0)
	enveloppe = ObjectProperty(1)
	transpo1 = ObjectProperty(0)
	transpo2 = ObjectProperty(0)
	transpo3 = ObjectProperty(0)
	
			
	def on_touch_up(self, touch):
		global transpo
		if tenu3 == 0:
			oscSendNote(3,0)
			self.marqueur3 = -35
		if tenu2 == 0:		
			self.marqueur2 = -35
			oscSendNote(2,0)
		if tenu1 == 0:		
			self.marqueur1 = -35
			oscSendNote(1,0)
		if touch.y>300:
			image=self.ids.transpo
			image.source = "images/transpo.png"
			transpo = 0
		
		
	def on_touch_down(self, touch):	
		global tenu1, tenu2, tenu3, mode, transpo, transpo1depart, transpo2depart, transpo3depart
		if touch.y<100:
			if touch.x<64:
				tenu3 = (tenu3 +1) %2
				image = self.ids.bouton3
				if tenu3 == 0:
					image.source = "images/bouton3.png"
				if tenu3 == 1:	
					image.source = "images/boutonEnfonce3.png"
			if touch.x>64:
				if transpo ==0:	
					oscSendNote(3,(touch.x/32)+36+self.transpo3/32.6)
					self.marqueur3 = touch.x
				if transpo ==1:
					transpo3depart = touch.x
		elif touch.y<200:
			if touch.x<64:
				tenu2 = (tenu2 +1) %2
				image = self.ids.bouton2
				if tenu2 == 0:
					image.source = "images/bouton2.png"
				if tenu2 == 1:	
					image.source = "images/boutonEnfonce2.png"
			if touch.x>64:
				if transpo ==0:	
					oscSendNote(2,(touch.x/32)+36+self.transpo2/32.6)
					self.marqueur2 = touch.x
				if transpo ==1:
					transpo2depart = touch.x
		elif touch.y<300:
			if touch.x<64:
				tenu1 = (tenu1 +1) %2
				image = self.ids.bouton1
				if tenu1 == 0:
					image.source = "images/bouton1.png"
				if tenu1 == 1:	
					image.source = "images/boutonEnfonce1.png"
			if touch.x>64:
				if transpo ==0:
					oscSendNote(1,(touch.x/32)+36+self.transpo1/32.6)
					self.marqueur1 = touch.x
				if transpo ==1:
					transpo1depart = touch.x
				
		else:
			if touch.x<180:
				if touch.y>368:
					image = self.ids.diagramme
					mode = (mode +1) %3
					if mode == 1:
						label = self.ids.labelIndice
						label.font_size = 0
						self.masque = 1
					else:
						label = self.ids.labelIndice
						label.font_size = 18
						self.masque = 0
					oscSendMode(mode)
					image.source = "images/diagramme"+str(mode)+".png"
				else:
					image=self.ids.transpo
					image.source = "images/transpoEnfonce.png"
					transpo = 1
			else:
				if touch.y<368:
					self.indice = (touch.x-200)/60
					oscSendIndice(self.indice)
				elif touch.y<424:
					self.enveloppe = (touch.x-200)/60
					oscSendEnv(self.enveloppe)
				else:
					self.volume = (touch.x-200)/60
					oscSendVol(self.volume*0.1)
				
	def on_touch_move(self, touch):
		global transpo1depart, transpo2depart, transpo3depart, transpo
		if touch.y<100:
			if touch.x>64:
				if transpo ==0:		
					oscSendNote(3,(touch.x/32)+36+self.transpo3/32.6)
					self.marqueur3 = touch.x
				if transpo ==1:
					oscSendNote(3,0)
					self.marqueur3 = -35
					self.transpo3 = min(max(self.transpo3 + (transpo3depart - touch.x),0),848)
					transpo3depart = touch.x
		elif touch.y<200:
			if touch.x>64:
				if transpo ==0:	
					oscSendNote(2,(touch.x/32)+36+self.transpo2/32.6)
					self.marqueur2 = touch.x
				if transpo ==1:
					oscSendNote(2,0)
					self.marqueur2 = -35
					self.transpo2 = min(max(self.transpo2 + (transpo2depart - touch.x),0),848)
					transpo2depart = touch.x
		elif touch.y<300:
			if touch.x>64:	
				if transpo ==0:	
					oscSendNote(1,(touch.x/32)+36+self.transpo1/32.6)
					self.marqueur1 = touch.x
				if transpo ==1:
					oscSendNote(1,0)
					self.marqueur1 = -35
					self.transpo1 = min(max(self.transpo1 + (transpo1depart - touch.x),0),848)
					transpo1depart = touch.x
		else:
			if touch.x>200:
				if touch.y<368:
					self.indice = (touch.x-200)/60
					oscSendIndice(self.indice)
				elif touch.y<424:
					self.enveloppe = (touch.x-200)/60
					oscSendEnv(self.enveloppe)
				else:
					self.volume = (touch.x-200)/60
					oscSendVol(self.volume*0.1)
		
	def update(self,dt):
		if quitter == 1:
			DroneApp.get_running_app().stop()

class DroneApp(App):
	def build(self):
		drone = DroneWidget()
		Clock.schedule_interval(drone.update, 1.0/60.0)
		return drone
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
	DroneApp().run()

