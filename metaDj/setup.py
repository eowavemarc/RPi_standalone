#en cas de modification des fichiers sons, il est necessaire de lancer ce script.
#il est obligatoire d'avoir 4 fichiers sons

import os

os.system('sox sons/son1.wav -b 16 temp/son1.wav')
os.system('sox sons/son2.wav -b 16 temp/son2.wav')
os.system('sox sons/son3.wav -b 16 temp/son3.wav')
os.system('sox sons/son4.wav -b 16 temp/son4.wav')

import wave
import struct
import OSC
import time

##############################
#
# Analyse des sons pour la selection mono/stereo
#
##############################

son1 = wave.open("/home/pi/metaDj/temp/son1.wav","rb")
channelNum1 = son1.getnchannels()
frameNum1 = son1.getnframes()
rate1 = son1.getframerate()
	
son2 = wave.open("temp/son2.wav","rb")
channelNum2 = son2.getnchannels()
frameNum2 = son2.getnframes()
rate2 = son2.getframerate()

son3 = wave.open("temp/son3.wav","rb")
channelNum3 = son3.getnchannels()
frameNum3 = son3.getnframes()
rate3 = son3.getframerate()

son4 = wave.open("temp/son4.wav","rb")
channelNum4 = son4.getnchannels()
frameNum4 = son4.getnframes()
rate4 = son4.getframerate()

def monoStereo(numSampler):
	if numSampler==1:
		channelNum = son1.getnchannels()
	if numSampler==2:
		channelNum = son2.getnchannels()
	if numSampler==3:
		channelNum = son3.getnchannels()
	if numSampler==4:
		channelNum = son4.getnchannels()
	return channelNum


	#####
	#calcul des 'rms' du son1
	#####

frameList1 = []
frameList1r = []
for i in range(frameNum1):
	frame = son1.readframes(1)
	framel = struct.unpack('<h',frame[0:2])
	frameList1.append(framel[0])
	if channelNum1 == 2:
		framer = struct.unpack('<h',frame[2:4])
		frameList1r.append(framer[0])

rmsList1 = []
rmsList1r = []
a=0
while (a<560):
	somme = 0
	for i in range(10):
		somme = somme+ abs(frameList1[i+a*len(frameList1)//560])
	somme = somme*0.0005
	rmsList1.append(somme)
	a = a + 1

a=0
while (a<560):
	somme = 0
	for i in range(10):
		somme = somme+ abs(frameList1r[i+a*len(frameList1r)//560])
	somme = somme*0.0005
	rmsList1r.append(somme)
	a = a + 1
					

	#####
	#calcul des 'rms' du son2
	#####

rmsList2 = []
rmsList2r = []
frameList2 = []
frameList2r = []
for i in range(frameNum2):
	frame = son2.readframes(1)
	framel = struct.unpack('<h',frame[0:2])
	frameList2.append(framel[0])
	if channelNum1 == 2:
		framer = struct.unpack('<h',frame[2:4])
		frameList2r.append(framer[0])
	
a=0
while (a<560):
	somme = 0
	for i in range(10):
		somme = somme+ abs(frameList2[i+a*len(frameList2)//560])
	somme = somme*0.0005
	rmsList2.append(somme)
	a = a + 1
	
a=0
while (a<560):
	somme = 0
	for i in range(10):
		somme = somme+ abs(frameList2r[i+a*len(frameList2r)//560])
	somme = somme*0.0005
	rmsList2r.append(somme)
	a = a + 1
	
	
	#####
	#calcul des 'rms' du son3
	#####

rmsList3 = []
rmsList3r = []
frameList3 = []
frameList3r = []
for i in range(frameNum3):
	frame = son3.readframes(1)
	framel = struct.unpack('<h',frame[0:2])
	frameList3.append(framel[0])
	if channelNum3 == 2:
		framer = struct.unpack('<h',frame[2:4])
		frameList3r.append(framer[0])
	
a=0
while (a<560):
	somme = 0
	for i in range(10):
		somme = somme+ abs(frameList3[i+a*len(frameList3)//560])
	somme = somme*0.0005
	rmsList3.append(somme)
	a = a + 1

a=0
while (a<560):
	somme = 0
	for i in range(10):
		somme = somme+ abs(frameList3r[i+a*len(frameList3r)//560])
	somme = somme*0.0005
	rmsList3r.append(somme)
	a = a + 1

		
			
	#####
	#calcul des 'rms' du son4
	#####

rmsList4 = []
rmsList4r = []
frameList4 = []
frameList4r = []
for i in range(frameNum4):
	frame = son4.readframes(1)
	framel = struct.unpack('<h',frame[0:2])
	frameList4.append(framel[0])
	if channelNum4 == 2:
		framer = struct.unpack('<h',frame[2:4])
		frameList4r.append(framer[0])
	
a=0
while (a<560):
	somme = 0
	for i in range(10):
		somme = somme+ abs(frameList4[i+a*len(frameList4)//560])
	somme = somme*0.0005
	rmsList4.append(somme)
	a = a + 1

a=0
while (a<560):
	somme = 0
	for i in range(10):
		somme = somme+ abs(frameList4r[i+a*len(frameList4r)//560])
	somme = somme*0.0005
	rmsList4r.append(somme)
	a = a + 1


#####################
#
# mise a jour des arrays
#
#####################

os.system("pd -nogui /home/pi/metaDj/gamepad.pd &")

time.sleep(10)

pd = ("localhost", 5000)
client = OSC.OSCClient()
client.connect( pd )

time.sleep(10)

client.sendto( OSC.OSCMessage("/setup", 1 ),pd )
client.sendto( OSC.OSCMessage("/init1", monoStereo(1) ),pd )
client.sendto( OSC.OSCMessage("/init2", monoStereo(2) ),pd )
client.sendto( OSC.OSCMessage("/init3", monoStereo(3) ),pd )
client.sendto( OSC.OSCMessage("/init4", monoStereo(4) ),pd )


####################
#
# ecriture dans le fichier temporaire
#
####################

ecriture = str(channelNum1)+"\n"+str(frameNum1)+"\n"+str(rate1)+"\n"+str(channelNum2)+"\n"+str(frameNum2)+"\n"+str(rate2)+"\n"+str(channelNum3)+"\n"+str(frameNum3)+"\n"+str(rate3)+"\n"+str(channelNum4)+"\n"+str(frameNum4)+"\n"+str(rate4)+"\n~\n"

for i in range(len(rmsList1)):
	ecriture = ecriture+str(rmsList1[i])+"\n"
ecriture = ecriture+"~\n"
for i in range(len(rmsList1r)):
	ecriture = ecriture+str(rmsList1r[i])+"\n"
ecriture = ecriture+"~\n"
for i in range(len(rmsList2)):
	ecriture = ecriture+str(rmsList2[i])+"\n"
ecriture = ecriture+"~\n"
for i in range(len(rmsList2r)):
	ecriture = ecriture+str(rmsList2r[i])+"\n"
ecriture = ecriture+"~\n"
for i in range(len(rmsList3)):
	ecriture = ecriture+str(rmsList3[i])+"\n"
ecriture = ecriture+"~\n"
for i in range(len(rmsList3r)):
	ecriture = ecriture+str(rmsList3r[i])+"\n"
ecriture = ecriture+"~\n"
for i in range(len(rmsList4)):
	ecriture = ecriture+str(rmsList4[i])+"\n"
ecriture = ecriture+"~\n"
for i in range(len(rmsList4r)):
	ecriture = ecriture+str(rmsList4r[i])+"\n"
	

fichier = open("/home/pi/metaDj/temp/var.txt","w")
fichier.write(ecriture)
fichier.close()
time.sleep(1)
os.system("pkill pd")
