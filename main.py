import pbc
import st7789
import random
import vga1_bold_16x16 as boldfont
import time

pb = pbc.PBC()

kreatur = 0
werte = [
        {
            "name": "Troll",
            "bild": "troll.png",
            "lep": 120,
            "lepmax": 120,
            "at": 13,
            "pa": 9,
            "tp": [3,12],
            "rs": 2
        },
		{
			"name": "Zant",
			"bild": "zant.png",
			"lep": 30,
			"lepmax": 40,
			"at": 16,
			"pa": 8,
			"tp": [1,5],
			"rs": 3
		},
		{
            "name": "Maru",
            "bild": "maru.png",
            "lep": 36,
            "lepmax": 36,
            "at": 14,
            "pa": 7,
            "tp": [1,3],
            "rs": 1
        },
        {
            "name": "Ork",
            "bild": "ork.png",
            "lep": 36,
            "lepmax": 36,
            "at": 12,
            "pa": 6,
            "tp": [1,3],
            "rs": 0
        },
        {
            "name": "Maraske",
            "bild": "maraske.png",
            "lep": 51,
            "lepmax": 51,
            "at": 9,
            "pa": 7,
            "tp": [1,3],
            "rs": 4
        }
    ]

def zeigebild():
    pb.tft.png('/'+werte[kreatur]["bild"],0,0)
    pb.tft.text(boldfont, werte[kreatur]["name"],240-(boldfont.WIDTH * len(werte[kreatur]["name"])) >> 1, 250)
    w = max(0,int(160*werte[kreatur]["lep"]/werte[kreatur]["lepmax"]))
    pb.tft.fill_rect(40,270,w,5,st7789.GREEN)
    pb.tft.fill_rect(40+w,270,160-w,5,st7789.RED)
    
def zeigeTP():
    pb.tft.text(boldfont, "TP: "+str(tp)+"   ",20,168)

zeigebild()

pressedA = False
pressedB = False
warteAufTP = False

while True:
    if pb.pressedLeft():
        if warteAufTP:
            tp = max(0,tp-1)
            zeigeTP()
            time.sleep_ms(250)
        else:
            kreatur = (kreatur+len(werte)-1) % len(werte)
            zeigebild()

    if pb.pressedRight():
        if warteAufTP:
            tp = min(100,tp+1)
            zeigeTP()
            time.sleep_ms(250)
        else:
            kreatur = (kreatur+1) % len(werte)
            zeigebild()
            
    if pb.pressedUp():
        werte[kreatur]["lep"] = werte[kreatur]["lepmax"]
        zeigebild()
        
    if pb.pressedCenter():
        if warteAufTP:
            werte[kreatur]["lep"] -= max(0,tp-werte[kreatur]["rs"])
            zeigebild()
            warteAufTP = False
            
        else:
            pb.tft.text(boldfont, "LE: "+str(werte[kreatur]["lep"]),20,20)
            pb.tft.text(boldfont, "AT: "+str(werte[kreatur]["at"]),20,36)
            pb.tft.text(boldfont, "PA: "+str(werte[kreatur]["pa"]),20,52)
            pb.tft.text(boldfont, "TP: "+str(werte[kreatur]["tp"][0])+"W6+"+str(werte[kreatur]["tp"][1]),20,68)
        
    if pb.pressedA() and not pressedA:
        pressedA = True
        wurf = random.randint(1,20)
        pb.tft.text(boldfont, "Wert: "+str(werte[kreatur]["at"])+" ",20,120)
        pb.tft.text(boldfont, "Wurf: "+str(wurf)+" ",20,136)
        if wurf<=werte[kreatur]["at"]:
            pb.tft.text(boldfont, "AT gelungen! ",20,152)
            tp = sum(random.randint(1, 6) for _ in range(werte[kreatur]["tp"][0]))+werte[kreatur]["tp"][1];
            pb.tft.text(boldfont, "TP: "+str(tp),20,168)
        else:
            pb.tft.text(boldfont, "AT misslungen!",20,152)
            pb.tft.text(boldfont, "       ",20,168)
    
    if pb.pressedB() and not pressedB:
        pressedB = True
        wurf = random.randint(1,20)
        pb.tft.text(boldfont, "Wert: "+str(werte[kreatur]["pa"])+" ",20,120)
        pb.tft.text(boldfont, "Wurf: "+str(wurf)+" ",20,136)
        if wurf<=werte[kreatur]["pa"]:
            pb.tft.text(boldfont, "PA gelungen! ",20,152)
            pb.tft.text(boldfont, "       ",20,168)
        else:
            pb.tft.text(boldfont, "PA misslungen!",20,152)
            warteAufTP = True
            tp = 0
            zeigeTP()
            
    if pressedA and not pb.pressedA():
        pressedA = False
        
    if pressedB and not pb.pressedB():
        pressedB = False
