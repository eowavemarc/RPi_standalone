import os
from Tkinter import *
import ser
import OSC
from threading import *			

##############################
#
# initialisation des serveur et client osc
#
##############################	
	
app = ("localhost", 4001)
client = OSC.OSCClient()
client.connect( app )

def oscSendStruct(materiel, liste):
	client.sendto(OSC.OSCMessage("/struct/"+materiel, liste), app)
	return()

def oscSendQuit():
	client.sendto(OSC.OSCMessage("/quit", 1), app)
	return()

receiveAdress = '127.0.0.1',4000
oscServer = OSC.ThreadingOSCServer(receiveAdress)
oscServer.addDefaultHandlers()

echo = 0
def printingHandler(addr, tags, stuff, source):
	global echo
	if addr=='/echo':
		echo = stuff[0]
oscServer.addMsgHandler('/echo',printingHandler)


##################
#
##################

def serial():
	while True:
		serialMsg = ser.serialLoop()
		if echo == 1:
			if serialMsg[0] == 176:
				oscSendStruct('bouton',serialMsg[1:3])
				if serialMsg[1] == 3:
					oscSendQuit()
			if serialMsg[0] > 127 and serialMsg[0] < 132:
				listTemp = [serialMsg[0]-127 , serialMsg[1]]
				oscSendStruct('encodeur',listTemp)
				
##################
#
##################

names = os.listdir("/home/pi")
paths = []
appNames = []
logos = []

for i in range(len(names)):
	if names[i] == names[i].replace('.',''):
		paths.append("/home/pi/"+str(names[i])+"/main.py")
		logos.append("/home/pi/"+str(names[i])+"/logo.ppm")
		appNames.append(names[i])
for i in range(12-len(paths)):
	paths.append(0)
	logos.append(0)
	appNames.append(0)

def echappement(event):
	fenetre.quit()


fenetre = Tk()
fond = Canvas(fenetre, width=800, height= 480, background="darkgray", cursor="none")	

def runApp(indice):
	os.system("/usr/bin/python "+str(paths[indice]))
def runApp0():runApp(0)
def runApp1():runApp(1)
def runApp2():runApp(2)
def runApp3():runApp(3)
def runApp4():runApp(4)
def runApp5():runApp(5)
def runApp6():runApp(6)
def runApp7():runApp(7)
def runApp8():runApp(8)
def runApp9():runApp(9)
def runApp9():runApp(10)
def runApp9():runApp(11)

grid = Frame(fenetre)
grid.grid(sticky=N+W+E+S, column=4, row=3)
for x in range(4):
	Grid.columnconfigure(fenetre, x, weight=1)
for y in range(3):
	Grid.rowconfigure(fenetre, y, weight=1)
	
try:
	paths[0] = int(paths[0])
except ValueError:
	try:
		logo0 = PhotoImage(file=logos[0])
		bouton0 = Button(fenetre,image=logo0, command=runApp0, cursor="none")
	except:
		bouton0 = Button(fenetre, text="lancer "+str(appNames[0]), command=runApp0, cursor="none")
	bouton0.grid(row=0, column=0)
try:
	paths[1] = int(paths[1])
except ValueError:	
	try:
		logo1 = PhotoImage(file=logos[1])
		bouton1 = Button(fenetre,image=logo1, command=runApp1, cursor="none")
	except:	
		bouton1 = Button(fenetre, text="lancer "+str(appNames[1]), command=runApp1, cursor="none")
	bouton1.grid(row=0, column=1)
try:
	paths[2] = int(paths[2])
except ValueError:
	try:
		logo2 = PhotoImage(file=logos[2])
		bouton2 = Button(fenetre,image=logo2, command=runApp2, cursor="none")
	except:
		bouton2 = Button(fenetre, text="lancer "+str(appNames[2]), command=runApp2, cursor="none")
	bouton2.grid(row=0, column=2)
try:
	paths[3] = int(paths[3])
except ValueError:
	try:
		logo3 = PhotoImage(file=logos[3])
		bouton3 = Button(fenetre,image=logo3, command=runApp3, cursor="none")
	except:
		bouton3 = Button(fenetre, text="lancer "+str(appNames[3]), command=runApp3, cursor="none")
	bouton3.grid(row=0, column=3)
try:
	paths[4] = int(paths[4])
except ValueError:
	try:
		logo4 = PhotoImage(file=logos[4])
		bouton4 = Button(fenetre,image=logo4, command=runApp4,cursor="none")
	except:
		bouton4 = Button(fenetre, text="lancer "+str(appNames[4]), command=runApp4, cursor="none")
	bouton4.grid(row=1, column=0)	
try:
	paths[5] = int(paths[5])
except ValueError:
	try:
		logo5 = PhotoImage(file=logos[5])
		bouton5 = Button(fenetre,image=logo5, command=runApp5,cursor="none")
	except:
		bouton5 = Button(fenetre, text="lancer "+str(appNames[5]), command=runApp5, cursor="none")
	bouton5.grid(row=1, column=1)
try:
	paths[6] = int(paths[6])
except ValueError:
	try:
		logo6 = PhotoImage(file=logos[6])
		bouton6 = Button(fenetre,image=logo6, command=runApp6,cursor="none")
	except:
		bouton6 = Button(fenetre, text="lancer "+str(appNames[6]), command=runApp6, cursor="none")
	bouton6.grid(row=1, column=2)
try:
	paths[7] = int(paths[7])
except ValueError:
	try:
		logo7 = PhotoImage(file=logos[7])
		bouton7 = Button(fenetre,image=logo7, command=runApp7,cursor="none")
	except:
		bouton7 = Button(fenetre, text="lancer "+str(appNames[7]), command=runApp7, cursor="none")
	bouton7.grid(row=1, column=3)
try:
	paths[8] = int(paths[8])
except ValueError:
	try:
		logo8 = PhotoImage(file=logos[8])
		bouton8 = Button(fenetre,image=logo8, command=runApp8,cursor="none")
	except:
		bouton8 = Button(fenetre, text="lancer "+str(appNames[8]), command=runApp8, cursor="none")
	bouton8.grid(row=2, column=0)
try:
	paths[9] = int(paths[9])
except ValueError:
	try:
		logo9 = PhotoImage(file=logos[9])
		bouton9 = Button(fenetre,image=logo9, command=runApp9,cursor="none")
	except:
		bouton9 = Button(fenetre, text="lancer "+str(appNames[9]), command=runApp9, cursor="none")	
	bouton9.grid(row=2, column=1)
try:
	paths[10] = int(paths[10])
except ValueError:
	try:
		logo10 = PhotoImage(file=logos[10])
		bouton10 = Button(fenetre,image=logo10, command=runApp10,cursor="none")
	except:
		bouton10 = Button(fenetre, text="lancer "+str(appNames[10]), command=runApp10, cursor="none")	
	bouton10.grid(row=2, column=2)
try:
	paths[11] = int(paths[11])
except ValueError:
	try:
		logo11 = PhotoImage(file=logos[11])
		bouton11 = Button(fenetre,image=logo11, command=runApp11,cursor="none")
	except:
		bouton11 = Button(fenetre, text="lancer "+str(appNames[11]), command=runApp11, cursor="none")	
	bouton11.grid(row=2, column=3)
	
fenetre.attributes("-fullscreen", True)
fenetre.bind("<Escape>",echappement)


#######################
#
serialThread = Thread(target=serial)
#
#######################

osc = Thread(target=oscServer.serve_forever)

if __name__ == '__main__':
	serialThread.start()
	osc.start()
	fenetre.mainloop()
