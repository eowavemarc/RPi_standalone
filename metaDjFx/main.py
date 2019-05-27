import os
os.system("pd -nogui /home/pi/metaDjFx/gamepad.pd &")

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

vol = [0.5]*3
rate = [0]*3
rateFixe = [1]*3
play = [0]*3
ratio = [0]*3
volrateAct = 0
lastPos = [0]*3
size = 640

frameListAdapt1 = [0]* 2 *size
for i in range(size):
	frameListAdapt1[2*i] = i + 160
frameListAdapt2 = [0]* 2*size
for i in range(size):
	frameListAdapt2[2*i] = i + 160
frameListAdapt3 = [0]* 2*size
for i in range(size):
	frameListAdapt3[2*i] = i + 160

fichier = open("/home/pi/metaDjFx/temp/var.txt","r")
data = fichier.read()
data = data.split("~")
rmsList1 = data[1]
rmsList1r = data[2]
rmsList2 = data[3]
rmsList2r = data[4]
rmsList3 = data[5]
rmsList3r = data[6]

rmsList1 = rmsList1.split("\n")
rmsList1r = rmsList1r.split("\n")
rmsList2 = rmsList2.split("\n")
rmsList2r = rmsList2r.split("\n")
rmsList3 = rmsList3.split("\n")
rmsList3r = rmsList3r.split("\n")

del rmsList1[0]
del rmsList1r[0]
del rmsList2[0]
del rmsList2r[0]
del rmsList3[0]
del rmsList3r[0]

del rmsList1[size]
del rmsList1r[size]
del rmsList2[size]
del rmsList2r[size]
del rmsList3[size]
del rmsList3r[size]

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
	
def oscSendDisto(reverb):
	client.sendto(OSC.OSCMessage("/mixDisto", reverb), pd)
	return()

def oscSendPhaser(index):
	client.sendto(OSC.OSCMessage("/mixPhaser", index), pd)
	return()
	
def oscSendFreq(index):
	client.sendto(OSC.OSCMessage("/freq", index), pd)
	return()
	
def oscSendLfo(index):
	client.sendto(OSC.OSCMessage("/rate", index), pd)
	return()
	
for i in range(3):
	oscSendRate(i+1,0)
	oscSendVol(i+1,vol[i])
	
def printingHandler(addr, tags, stuff, source):
	global ratio
	if addr=='/index':
		for i in range(3):
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
	vol1 = ObjectProperty(10)
	vol2 = ObjectProperty(10)
	vol3 = ObjectProperty(10)
	rate = ObjectProperty(0)
	zero1 = ObjectProperty(0)
	zero2 = ObjectProperty(0)
	zero3 = ObjectProperty(0)
	alpha = ObjectProperty(0)
	posXeffect1 = ObjectProperty(-35)
	posYeffect1 = ObjectProperty(-35)
	posXeffect2 = ObjectProperty(-35)
	posYeffect2 = ObjectProperty(-35)
	hauteurRate = ObjectProperty(500)

#########################################	
	def on_touch_up(self, touch):
		global volrateAct, rate
		
		if volrateAct > 4:
			if volrateAct ==5:
				image = self.ids.imageVolrate1
				image.source = "images/volrate.png"
			if volrateAct ==6:
				image = self.ids.imageVolrate2
				image.source = "images/volrate.png"
			if volrateAct ==7:
				image = self.ids.imageVolrate3
				image.source = "images/volrate.png"
			self.ids.imageRateRegle.size=(800,0)
			self.hauteurRate=500
			self.ids.rate.font_size=0
			self.alpha = 0
			volrateAct = 0
		elif volrateAct != 0:
			self.ids.imageRateRegle.size=(800,80)
			self.ids.rate.font_size=16
			self.alpha = 0.1
			self.hauteurRate = 160 + 80*volrateAct
			self.ids.rate.center_y= 220 + 80*volrateAct
			self.rate = rateFixe[volrateAct-1]
			self.ids.rate.center_x=(rateFixe[volrateAct-1]+2)*200+40
			volrateAct = volrateAct + 4
		for i in range(3):
			oscSendRate(i+1, rate[i])
		
##################################		
	def on_touch_down(self, touch):		
		global volrateAct, rate, indexAct, vol, play, rateFixe, lastPos
		if volrateAct != 0:
			self.ids.rate.center_x=touch.x+40
			self.rate = (int(touch.x/20-20))*0.1
			rate[volrateAct-5] = (touch.x/200)-2
			oscSendRate(volrateAct-4,rate[volrateAct-5])
				
		elif volrateAct ==0:
			if touch.y<240:
				yCalcul = max(min((touch.y-15),200),10)
				if touch.x<53:
					self.vol1= yCalcul
					oscSendVol(3, (yCalcul-10)/190)
				elif touch.x<106:
					self.vol2=yCalcul
					oscSendVol(2, (yCalcul-10)/190)
				elif touch.x<160:
					self.vol3=yCalcul
					oscSendVol(1, (yCalcul-10)/190)
				elif touch.x<480:
					self.posXeffect1 = max(min(touch.x-15,450),160)
					self.posYeffect1 = max(min(touch.y-15,210),0)
					oscSendDisto(max(min((touch.x-175)/275,1),0))
					oscSendFreq(max((touch.y)*20,0))
				else:
					self.posXeffect2 = max(min(touch.x-15,770),480)
					self.posYeffect2 = max(min(touch.y-15,210),0)
					oscSendPhaser(max(min((touch.x-495)/275,1),0))
					oscSendLfo(max(min((touch.y-15)/195,1),0))
			elif touch.x<80:
				playSel = max(int(touch.y-241)/80+1,1)
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
			elif touch.x<160:
				if touch.y<320:
					image = self.ids.imageVolrate1
					volrateAct = 1
					image.source = "images/volrateActif.png"	
				elif touch.y<400:
					image = self.ids.imageVolrate2
					volrateAct = 2
					image.source = "images/volrateActif.png"	
				else:
					image = self.ids.imageVolrate3
					volrateAct = 3
					image.source = "images/volrateActif.png"
					
			else:
				lastPos[max(int(touch.y-241)/80,0)] = touch.x
		
##########################################	
	def on_touch_move(self, touch):
		global volrateAct, vol, rate, play, lastPos, rateFixe
		if volrateAct !=0:
			self.ids.rate.center_x=touch.x+40
			self.rate = int(touch.x/20-20)*0.1
			if volrateAct < 5:
				self.ids.imageRateRegle.size=(800,80)
				self.ids.rate.font_size=16
		
		if volrateAct ==0:
			if touch.y<240:
				yCalcul = max(min((touch.y-15),200),10)
				if touch.x<53:
					self.vol1= yCalcul
					oscSendVol(3, (yCalcul-10)/190)
				elif touch.x<106:
					self.vol2=yCalcul
					oscSendVol(2, (yCalcul-10)/190)
				elif touch.x<160:
					self.vol3=yCalcul
					oscSendVol(1, (yCalcul-10)/190)
				elif touch.x<480:
					self.posXeffect1 = max(min(touch.x-15,450),160)
					self.posYeffect1 = max(min(touch.y-15,210),0)
					oscSendDisto(max(min((touch.x-175)/275,1),0))
					oscSendFreq(max((touch.y)*20,0))
				else:
					self.posXeffect2 = max(min(touch.x-15,770),480)
					self.posYeffect2 = max(min(touch.y-15,210),0)
					oscSendPhaser(max(min((touch.x-495)/275,1),0))
					oscSendLfo(max(min((touch.y-15)/195,1),0))
			else:
				rate[max(int(touch.y-241)/80,0)] = (lastPos[max(int(touch.y-241)/80,0)] - touch.x)/20
				lastPos[max(int(touch.y-241)/80,0)] = touch.x
		
		
		elif volrateAct > 4:
			rateFixe[volrateAct-5] = (touch.x/200)-2
		
		else:
			volrateAct = volrateAct + 4	
		
		
		
###############################		
	def update(self,dt):
		global quitter, rateFixe, frameListAdapt1, frameListAdapt2, frameListAdapt3, rmsList1, rmsList1r, rmsList2, rmsList2r, rmsList3, rmsList3r, rate, lastPos, play
		
		self.zero1 = 800 - (ratio[0]*2+ (size*0.5))%(2*size)
		self.zero2 = 800 - (ratio[1]*2+ (size*0.5))%(2*size)
		self.zero3 = 800 - (ratio[2]*2+ (size*0.5))%(2*size)
		
		for i in range(3):
			rate[i] = min(max(rate[i],-100),100)
			oscSendRate(i+1, rate[i])
			rate[i] = rate[i] - (rate[i]-rateFixe[i]*play[i])*0.02
		
		for i in range(int(size*0.5)):
			frameListAdapt1[4*i+1] = 280 + rmsList1[(i+ratio[0]-140)%size]
			frameListAdapt1[4*i+3] =  280 - rmsList1r[(i+ratio[0]-140)%size]	
		self.table1 = frameListAdapt1
		
		for i in range(int(size*0.5)):
			frameListAdapt2[4*i+1] = 360 + rmsList2[(i+ratio[1]-140)%size]
			frameListAdapt2[4*i+3] = 360 - rmsList2r[(i+ratio[1]-140)%size]	
		self.table2 = frameListAdapt2
		
		for i in range(int(size*0.5)):
			frameListAdapt3[4*i+1] = 440 + rmsList3[(i+ratio[2]-140)%size]
			frameListAdapt3[4*i+3] = 440 - rmsList3r[(i+ratio[2]-140)%size]	
		self.table3 = frameListAdapt3
		
		if quitter == 1:
			GrilleApp.get_running_app().stop()
						

class GrilleApp(App):
	def build(self):
		grille = GrilleWidget()
		Clock.schedule_interval(grille.update, 1.0/60.0)
		return grille
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
	GrilleApp().run()

