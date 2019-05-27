import os
os.system("pd -nogui /home/pi/metaDj/gamepad.pd &")

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

vol = [0.5]*4
rate = [0]*4
rateFixe = [1]*4
play = [0]*4
ratio = [0]*4
volrateAct = 0
lastPos = [0]*4


frameListAdapt1 = [0]* 1120
for i in range(560):
	frameListAdapt1[2*i] = i + 240
frameListAdapt2 = [0]* 1120
for i in range(560):
	frameListAdapt2[2*i] = i + 240
frameListAdapt3 = [0]* 1120
for i in range(560):
	frameListAdapt3[2*i] = i + 240
frameListAdapt4 = [0]* 1120
for i in range(560):
	frameListAdapt4[2*i] = i + 240

fichier = open("/home/pi/metaDj/temp/var.txt","r")
data = fichier.read()
data = data.split("~")
rmsList1 = data[1]
rmsList1r = data[2]
rmsList2 = data[3]
rmsList2r = data[4]
rmsList3 = data[5]
rmsList3r = data[6]
rmsList4 = data[7]
rmsList4r = data[8]

rmsList1 = rmsList1.split("\n")
rmsList1r = rmsList1r.split("\n")
rmsList2 = rmsList2.split("\n")
rmsList2r = rmsList2r.split("\n")
rmsList3 = rmsList3.split("\n")
rmsList3r = rmsList3r.split("\n")
rmsList4 = rmsList4.split("\n")
rmsList4r = rmsList4r.split("\n")

del rmsList1[0]
del rmsList1r[0]
del rmsList2[0]
del rmsList2r[0]
del rmsList3[0]
del rmsList3r[0]
del rmsList4[0]
del rmsList4r[0]

del rmsList1[560]
del rmsList1r[560]
del rmsList2[560]
del rmsList2r[560]
del rmsList3[560]
del rmsList3r[560]
del rmsList4[560]
del rmsList4r[560]

for i in range(len(rmsList1)):
	rmsList1[i] = float(rmsList1[i])
for i in range(len(rmsList1r)):
	rmsList1r[i] = float(rmsList1r[i])
	
for i in range(len(rmsList2)):
	rmsList2[i] = float(rmsList2[i])
for i in range(len(rmsList2r)):
	rmsList2r[i] = float(rmsList2r[i])
	
for i in range(len(rmsList3)):
	rmsList3[i] = float(rmsList3[i])
for i in range(len(rmsList3r)):
	rmsList3r[i] = float(rmsList3r[i])
	
for i in range(len(rmsList4)):
	rmsList4[i] = float(rmsList4[i])
for i in range(len(rmsList4r)):
	rmsList4r[i] = float(rmsList4r[i])

data = data[0].split("\n")
fichier.close()

def playing(numSampler):
	play[numSampler-1] = (play[numSampler-1]+1)%2
	if play[numSampler-1] == 1:
		rate[numSampler-1] = rateFixe[numSampler-1]	
	if play[numSampler-1] == 0:
		rate[numSampler-1] = 0
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


def oscSendRate(numSampler, rate):
	client.sendto(OSC.OSCMessage("/lecteur"+str(numSampler)+"/rate", rate), pd)
	return()
	
def oscSendVol(numSampler, vol):
	client.sendto(OSC.OSCMessage("/lecteur"+str(numSampler)+"/volume", vol), pd)
	return()

for i in range(4):
	oscSendRate(i+1,0)
	oscSendVol(i+1,vol[i])

def printingHandler(addr, tags, stuff, source):
	global ratio
	if addr=='/index':
		for i in range(4):
			ratio[i] = stuff[i]
oscServer.addMsgHandler('/index',printingHandler)

##############################
#
# application kivy
#
##############################

class GrilleWidget(Widget):
	table1 = ListProperty(0)
	table2 = ListProperty(0)
	table3 = ListProperty(0)
	table4 = ListProperty(0)
	volume = ObjectProperty(0)
	rate = ObjectProperty(0)
	zero1 = ObjectProperty(0)
	zero2 = ObjectProperty(0)
	zero3 = ObjectProperty(0)
	zero4 = ObjectProperty(0)
	alpha1 = ObjectProperty(0)
	alpha2 = ObjectProperty(0)
	alpha3 = ObjectProperty(0)
	alpha4 = ObjectProperty(0)

#########################################	
	def on_touch_up(self, touch):
		global volrateAct, rate
		
		if volrateAct > 4:
			self.alpha1 = 0
			self.alpha2 = 0
			self.alpha3 = 0
			self.alpha4 = 0
			if volrateAct ==5:
				image = self.ids.imageVolrate1
				image.source = "images/volrate.png"
			if volrateAct ==6:
				image = self.ids.imageVolrate2
				image.source = "images/volrate.png"
			if volrateAct ==7:
				image = self.ids.imageVolrate3
				image.source = "images/volrate.png"
			if volrateAct ==8:
				image = self.ids.imageVolrate4
				image.source = "images/volrate.png"
			self.ids.niveau.font_size=0
			self.ids.imageNiveau.size=(0,480)
			self.ids.imageRateRegle.size=(800,0)
			self.ids.rate.font_size=0
			volrateAct = 0
		elif volrateAct != 0:
			self.ids.niveau.font_size=16
			self.ids.imageNiveau.size=(10,480)
			self.ids.imageRateRegle.size=(800,12)
			self.ids.rate.font_size=16
			self.ids.imageNiveau.center_x=(rateFixe[volrateAct-1]+2)*200
			self.ids.niveau.center_x=(rateFixe[volrateAct-1]+2)*200-40
			self.ids.rate.center_x=(rateFixe[volrateAct-1]+2)*200+40
			self.rate = (int(10*rateFixe[volrateAct-1]))*0.1
			self.ids.niveau.center_y=vol[volrateAct-1]*480+40
			self.ids.imageRateRegle.center_y=vol[volrateAct-1]*480
			self.ids.rate.center_y=vol[volrateAct-1]*480+40
			self.volume = int(10*vol[volrateAct-1])
		if volrateAct==1:
			self.alpha1 = 0.2
			self.alpha2 = 0.5
			self.alpha3 = 0.5
			self.alpha4 = 0.5
			volrateAct=5
		if volrateAct==2:
			self.alpha1 = 0.5
			self.alpha2 = 0.2
			self.alpha3 = 0.5
			self.alpha4 = 0.5
			volrateAct=6
		if volrateAct==3:
			self.alpha1 = 0.5
			self.alpha2 = 0.5
			self.alpha3 = 0.2
			self.alpha4 = 0.5
			volrateAct=7
		if volrateAct==4:
			self.alpha1 = 0.5
			self.alpha2 = 0.5
			self.alpha3 = 0.5
			self.alpha4 = 0.2
			volrateAct=8
		
		
##################################		
	def on_touch_down(self, touch):		
		global rateFixe, play, volrateAct, rate, vol, lastPos
		if volrateAct != 0:
			self.ids.imageNiveau.center_x=touch.x
			self.ids.niveau.center_y=touch.y+40
			self.ids.niveau.center_x=touch.x-40
			self.ids.imageRateRegle.center_y=touch.y
			self.ids.rate.center_y=touch.y+40
			self.ids.rate.center_x=touch.x+40
			self.volume = int(touch.y/48)
			self.rate = (int(touch.x/20-20))*0.1
			
			if volrateAct > 4:
				vol[volrateAct-5] = touch.y/480
				oscSendVol(volrateAct-4,vol[volrateAct-5])
				rateFixe[volrateAct-5] = (touch.x/200)-2
				
				
		elif volrateAct == 0:		
			if touch.x<120:
				playSel = int(touch.y/121)+1
				playing(playSel)
				if playSel == 1:
					image = self.ids.imagePlay1
					if play[0] == 0:
						image.source = "images/play.png"
					if play[0] == 1:
						image.source = "images/pause.png"
				if playSel == 2:
					image = self.ids.imagePlay2
					if play[1] == 0:
						image.source = "images/play.png"
					if play[1] == 1:
						image.source = "images/pause.png"
				if playSel == 3:
					image = self.ids.imagePlay3
					if play[2] == 0:
						image.source = "images/play.png"
					if play[2] == 1:
						image.source = "images/pause.png"
				if playSel == 4:
					image = self.ids.imagePlay4
					if play[3] == 0:
						image.source = "images/play.png"
					if play[3] == 1:
						image.source = "images/pause.png"
			elif touch.x<240:
				if touch.y<120:
					image = self.ids.imageVolrate1
					volrateAct = 1
					image.source = "images/volrateActif.png"	
				elif touch.y<240:
					image = self.ids.imageVolrate2
					volrateAct = 2
					image.source = "images/volrateActif.png"	
				elif touch.y<360:
					image = self.ids.imageVolrate3
					volrateAct = 3
					image.source = "images/volrateActif.png"	
				else:
					image = self.ids.imageVolrate4
					volrateAct = 4
					image.source = "images/volrateActif.png"
					
			else:
				lastPos[int(touch.y/121)] = touch.x
				
				
##########################################	
	def on_touch_move(self, touch):
		global volrateAct, vol, rate, play, lastPos, rateFixe
		if volrateAct == 0:
			rate[int(touch.y/121)] = (lastPos[int(touch.y/121)] - touch.x)/20
			lastPos[int(touch.y/121)] = touch.x
					
		elif volrateAct > 4:
			vol[volrateAct-5] = touch.y/480
			oscSendVol(volrateAct-4,vol[volrateAct-5])
			rateFixe[volrateAct-5] = (touch.x/200)-2
			
		else:
			volrateAct = volrateAct + 4
			self.ids.niveau.font_size=16
			self.ids.imageNiveau.size=(10,480)
			self.ids.imageRateRegle.size=(800,12)
			self.ids.rate.font_size=16	
		
		if volrateAct !=0:
			self.ids.imageNiveau.center_x=touch.x
			self.ids.niveau.center_y=touch.y+40
			self.ids.niveau.center_x=touch.x-40
			self.ids.imageRateRegle.center_y=touch.y
			self.ids.rate.center_y=touch.y+40
			self.ids.rate.center_x=touch.x+40
			self.volume = int(touch.y/48)
			self.rate = int(touch.x/20-20)*0.1
				
		
###############################		
	def update(self,dt):
		global quitter, rateFixe, frameListAdapt1, frameListAdapt2, frameListAdapt3, frameListAdapt4, rmsList1, rmsList1r, rmsList2, rmsList2r, rmsList3, rmsList3r, rmsList4, rmsList4r, rate, lastPos, play
		
		self.zero1 = 800 - (ratio[0]*2+ 280)%1120
		self.zero2 = 800 - (ratio[1]*2+ 280)%1120
		self.zero3 = 800 - (ratio[2]*2+ 280)%1120
		self.zero4 = 800 - (ratio[3]*2+ 280)%1120
		
		for i in range(4):
			rate[i] = min(max(rate[i],-100),100)
			oscSendRate(i+1, rate[i])
			rate[i] = rate[i] - (rate[i]-rateFixe[i]*play[i])*0.02
		
		
		for i in range(280):
			frameListAdapt1[4*i+1] = 60 + rmsList1[(i+ratio[0]-140)%560]
			frameListAdapt1[4*i+3] =  60 - rmsList1r[(i+ratio[0]-140)%560]	
		self.table1 = frameListAdapt1
		
		for i in range(280):
			frameListAdapt2[4*i+1] = 180 + rmsList2[(i+ratio[1]-140)%560]
			frameListAdapt2[4*i+3] = 180 - rmsList2r[(i+ratio[1]-140)%560]	
		self.table2 = frameListAdapt2
		
		for i in range(280):
			frameListAdapt3[4*i+1] = 300 + rmsList3[(i+ratio[2]-140)%560]
			frameListAdapt3[4*i+3] = 300 - rmsList3r[(i+ratio[2]-140)%560]	
		self.table3 = frameListAdapt3
		
		for i in range(280):
			frameListAdapt4[4*i+1] = 420 + rmsList4[(i+ratio[3]-140)%560]
			frameListAdapt4[4*i+3] = 420 - rmsList4r[(i+ratio[3]-140)%560]	
		self.table4 = frameListAdapt4
		
		if quitter == 1:
			GrilleApp.get_running_app().stop()
						

class GrilleApp(App):
	def build(self):
		grille = GrilleWidget()
		Clock.schedule_interval(grille.update, 1.0/60.0)
		return grille
	def on_stop(self):
		client.sendto(OSC.OSCMessage("/echo", 0), hub)
		oscServerHub.close()
		client.sendto( OSC.OSCMessage("/close", 1 ),pd )
		oscServer.close()
		os.system("pkill pd")


##############################
#
# lancement des thread osc et kivy
#
##############################

osc = Thread(target=oscServer.serve_forever)
oscHub =  Thread(target=oscServerHub.serve_forever)

if __name__ == '__main__':
	oscHub.start()
	osc.start()
	GrilleApp().run()

