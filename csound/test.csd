<CsoundSynthesizer>
<CsOptions>
-odac -Ma --midi-key-cps=4 --midi-velocity-amp=5 -
</CsOptions>
<CsInstruments>

sr = 44100
ksmps = 64
nchnls = 2
0dbfs = 1.0
massign 0, 1

gihandle OSCinit 5002
gkatt init 0
gkrel init 0
gkVol init 0
gkRes init 0
gkCutoff init 0
gkenvMod init 0
gkmix init 0
gkrate init 0
giatt init 0
girel init 0
gaEffect init 0


instr 1

OSCsend 1, "localhost",5003, "/midi", "f", p4
iAmp =  log10((p5*9)+1)
iFreq = p4

iatt = i(gkatt)
irel = i(gkrel)
iattx = (exp(iatt)-0.99)
irelx= (exp(irel)-0.99)

kEnv madsr iattx, 0, 1, irelx
aVco vco2 iAmp, iFreq

gkvol = exp(gkVol)-1

aFil moogladder aVco, gkCutoff * (1 -(1-kEnv)*gkenvMod), gkRes

gaEffect= gaEffect + aFil * kEnv * gkvol

endin

instr 2

;nxtmsg:
gkans1 OSClisten gihandle, "/volume", "f", gkVol
gkans2 OSClisten gihandle, "/cutoff", "f", gkCutoff
gkans3 OSClisten gihandle, "/resonnance", "f", gkRes
gkans4 OSClisten gihandle, "/attaque", "f", gkatt
gkans5 OSClisten gihandle, "/release", "f", gkrel
gkans6 OSClisten gihandle, "/envMod", "f", gkenvMod
gkans7 OSClisten gihandle, "/mix", "f", gkmix
gkans8 OSClisten gihandle, "/rate", "f", gkrate
;if (gkans1==0) goto ex
;printk 0, gkVol
;kgoto nxtmsg
;ex:

kLfo oscil 0.5, gkrate*10
kLfo = kLfo + 0.5

aOutL = gaEffect * (1-(1-kLfo)*gkmix)*0.1
aOutR = gaEffect * (1-kLfo*gkmix)*0.1

aRevOutL, aRevOutR freeverb aOutL,aOutR, 0.2, 0.3
out aRevOutL+aOutL, aRevOutL+aOutR
clear gaEffect
endin

</CsInstruments>
<CsScore>
;f0 3600
i 2 0 3600
</CsScore>
</CsoundSynthesizer>
<bsbPanel>
 <label>Widgets</label>
 <objectName/>
 <x>100</x>
 <y>100</y>
 <width>320</width>
 <height>240</height>
 <visible>true</visible>
 <uuid/>
 <bgcolor mode="nobackground">
  <r>255</r>
  <g>255</g>
  <b>255</b>
 </bgcolor>
</bsbPanel>
<bsbPresets>
</bsbPresets>
