import serial
import struct

ser = serial.Serial(port='/dev/ttyS0',baudrate=115200)

def serialLoop():
	seri = [0]*3
	while True:
		line = ser.read()
		line = struct.unpack('B',line)
                if line[0] > 127:
                        seri[0] = line[0]
                        line = ser.read()
                        line = struct.unpack('B',line)
                        if line[0] < 128:
                                seri[1] = line[0]
                                line = ser.read()
                                line = struct.unpack('B',line)
                                if line[0] < 128:
                                        seri[2]= line[0]
                                        return(seri)
