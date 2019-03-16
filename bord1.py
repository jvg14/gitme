from itertools import cycle
import random
import time
import sys
import pygame
from pygame.locals import *

FPS = 30
breidd  = 576
haed = 512

# Myndir og hljóð dictionary
myndir, hljod = {}, {}


try:
    xrange
except NameError:
    xrange = range

class Bord1:
    def Opnunargluggi(self):
        # Sýnir upphafsgluggan fyrir borð 2
        leikmadurIndex = 0
        leikmadurIndexGen = cycle([0, 1, 2, 1])
        # Loopiter breytir leikmadurindex eftir hverja fimmtu ítrun
        loopIter = 0

        leikmadurx = int(breidd * 0.2)
        leikmadury = int((haed - myndir["leikmadur"][0].get_height()) / 2)

        skilabodx = int((breidd - myndir["skilabod"].get_width()) / 2)
        skilabody = int(haed * 0.12)

        # LeikmadurVals fyrir upp og niður hreyfingar á valmyndinni
        leikmadurVals = {"val": 0, "dir": 1}

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    # Framkvæmi fyrstu hljóð og skila fyrir leikinn
                    return {
                        "leikmadury": leikmadury + leikmadurVals["val"],
                        "leikmadurIndexGen": leikmadurIndexGen,
                    }

            # Lagfæra leikmadury, leikmadurIndex
            if (loopIter + 1) % 5 == 0:
                leikmadurIndex = next(leikmadurIndexGen)
            loopIter = (loopIter + 1) % 30
            self.leikmadurValmynd(leikmadurVals)

            # Teikna
            skjar.blit(myndir["bakgrunnur"], (0,0))
            skjar.blit(myndir["leikmadur"][0],
                        (leikmadurx, leikmadury + leikmadurVals["val"]))
            skjar.blit(myndir["skilabod"], (skilabodx, skilabody))

            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def leikur(self, hreyfingar, stada):
        # Fæ random staðsetningu á pening
        nyrpeningur1 = self.Random_Peningur()

        # Listi fyrir peninga
        Peningar = [
            {"z": nyrpeningur1[0]["z"], "x": nyrpeningur1[0]["x"], "y": nyrpeningur1[0]["y"]},
        ]
        time_elapsed_since_last_action = 0
        timisidan = 0
        timi=60
        timinn="60"
        clock = pygame.time.Clock()
        t = pygame.time.Clock()

        Leikmadury=236
        Leikmadurx=117
        Leikmadurxmin=0
        Leikmadurymin=0
        Leikmadurxmax=540
        Leikmadurymax=486
        LeikmadurVel=10
        pressed_up=False
        pressed_down=False
        pressed_right=False
        pressed_left=False

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_UP:
                    pressed_up = True
                if event.type == KEYDOWN and event.key == K_DOWN:
                    pressed_down = True
                if event.type == KEYDOWN and event.key == K_RIGHT:
                    pressed_right = True
                if event.type == KEYDOWN and event.key == K_LEFT:
                    pressed_left = True
                if event.type == KEYUP and event.key == K_UP:
                    pressed_up = False
                if event.type == KEYUP and event.key == K_DOWN:
                    pressed_down = False
                if event.type == KEYUP and event.key == K_RIGHT:
                    pressed_right = False
                if event.type == KEYUP and event.key == K_LEFT:
                    pressed_left = False

            # Ath. eftir árekstri
            arekst_prof = self.ath_arekstur(Leikmadurx, Leikmadury, Peningar)
            if arekst_prof:
                stada=stada+1

            et = t.tick()
            timisidan += et
            if timisidan > 1000:
                timi=timi-1
                timinn=str(timi)
                if timi <=0:
                    return stada
                timisidan=0

            dt = clock.tick()
            time_elapsed_since_last_action += dt
            if time_elapsed_since_last_action > 500:
                nyrpeningur = self.Random_Peningur()
                Peningar.append(nyrpeningur[0])
                time_elapsed_since_last_action = 0

            if pressed_up:
                Leikmadury -= LeikmadurVel
                if Leikmadury < Leikmadurymin:
                    Leikmadury = Leikmadurymin
            if pressed_down:
                Leikmadury += LeikmadurVel
                if Leikmadury > Leikmadurymax:
                    Leikmadury = Leikmadurymax
            if pressed_right:
                Leikmadurx += LeikmadurVel
                if Leikmadurx > Leikmadurxmax:
                    Leikmadurx = Leikmadurxmax
            if pressed_left:
                Leikmadurx -= LeikmadurVel
                if Leikmadurx < Leikmadurxmin:
                    Leikmadurx = Leikmadurxmin

            # Teikna
            skjar.blit(myndir["bakgrunnur"], (0,0))
            self.Syna_stodu(stada)
            font = pygame.font.Font('freesansbold.ttf',18)
            texti = font.render(timinn, True, (0,0,0))
            skjar.blit(texti, (275,125))

            for nyrpeningur1 in Peningar:
                # Vel random pening
                randpen = random.randint(0, 4)
                skjar.blit(myndir["peningar"][nyrpeningur1["z"]], (nyrpeningur1["x"], nyrpeningur1["y"]))

            skjar.blit(myndir["leikmadur"][0], (Leikmadurx,Leikmadury))

            pygame.display.update()
            FPSCLOCK.tick(FPS)


    def leikmadurValmynd(self, leikmadurValmynd): # Sama fall og borð 2 notar
          # Lætur gildið af LeikmadurValmynd flakka á milli -8 og 8
        if abs(leikmadurValmynd["val"]) == 8:
            leikmadurValmynd["dir"] *= -1

        if leikmadurValmynd["dir"] == 1:
             leikmadurValmynd["val"] += 1
        else:
            leikmadurValmynd["val"] -= 1

    def Random_Peningur(self):
        # Skilar random pening
        # Staðsetning penings
        Stad_x = random.randint(50, breidd-50)
        Stad_y = random.randint(23, haed-23)
        Mynd = random.randint(0, 4)
        return [
            {"z": Mynd ,"x": Stad_x, "y": Stad_y},
        ]
    def ath_arekstur(self, Leikmadurx, Leikmadury, Peningar):
        # Skila true ef árekstur verður á milli leikmanns og penings
        leikmadurb = myndir["leikmadur"][0].get_width()
        leikmadurh = myndir["leikmadur"][0].get_height()

        leikmadurhnit = pygame.Rect(Leikmadurx, Leikmadury, leikmadurb, leikmadurh)
        Peningarb = myndir["peningar"][0].get_width()
        Peningarh = myndir["peningar"][0].get_height()
        x=0
        for penge in Peningar:
            # Efri og neðri súlu hnit
            Peningahnit = pygame.Rect(penge["x"], penge["y"], Peningarb, Peningarh)


            # Hvort árekstur verður við pening
            arekstur = self.VardArekstur(leikmadurhnit, Peningahnit)

            if arekstur:
                Peningar.pop(x)
                x=0
                return True
            x=x+1
        x=0
        return False

    def VardArekstur(self, hnit1, hnit2):
        #Ath. hvort tveir hlutir klessa á hvorn annan
        x=False
        y=False
        xlag = hnit1.x-(hnit1.width)/2.0
        xhag = hnit1.x+(hnit1.width)/2.0
        xmin = hnit2.x-(hnit2.width)/2.0
        xmax = hnit2.x+(hnit2.width)/2.0
        ylag = hnit1.y-(hnit1.width)/2.0
        yhag = hnit1.y+(hnit1.width)/2.0
        ymin = hnit2.y-(hnit2.width)/2.0
        ymax = hnit2.y+(hnit2.width)/2.0
        if xhag <= xmax and xhag >= xmin:
            x=True
        if xlag <= xmax and xhag >= xmin:
            x=True
        if yhag <= ymax and yhag >= ymin:
            y=True
        if ylag <= ymax and yhag >= ymin:
            y=True

        if y and x:
            return True
        else:
            return False

    def Syna_stodu(self, stada):
        # Sýni stöðu í miðjum skjánum
        if stada<0:
            minus=True
            stada=stada*-1
        else:
            minus=False
        stadaDigits = [int(x) for x in list(str(stada))]
        totalWidth = 0 # Heildar breidd af öllum númerum sem verða prentuð

        for digit in stadaDigits:
            totalWidth += myndir["numer"][digit].get_width()

        Xoffset = (breidd - totalWidth) / 2
        Xupph = Xoffset-30
        for digit in stadaDigits:
            skjar.blit(myndir["numer"][digit], (Xoffset, haed * 0.1))
            Xoffset += myndir["numer"][digit].get_width()
        skjar.blit(myndir["auka"][1], (Xoffset, haed * 0.095))

        if minus:
            skjar.blit(myndir["auka"][0], (Xupph, haed * 0.12))

    def keyrsla(self):
        global skjar, FPSCLOCK
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        skjar = pygame.display.set_mode((breidd, haed))
        pygame.display.set_caption("Borð 1")


        # Myndin fyrir opnunargluggan
        myndir["skilabod"] = pygame.image.load("myndirnarb1/Valmynd.png").convert_alpha()

        # Númerin fyrir stöðutöfluna
        myndir["numer"] = (
            pygame.image.load("myndirnarb2/0.png").convert_alpha(),
            pygame.image.load("myndirnarb2/1.png").convert_alpha(),
            pygame.image.load("myndirnarb2/2.png").convert_alpha(),
            pygame.image.load("myndirnarb2/3.png").convert_alpha(),
            pygame.image.load("myndirnarb2/4.png").convert_alpha(),
            pygame.image.load("myndirnarb2/5.png").convert_alpha(),
            pygame.image.load("myndirnarb2/6.png").convert_alpha(),
            pygame.image.load("myndirnarb2/7.png").convert_alpha(),
            pygame.image.load("myndirnarb2/8.png").convert_alpha(),
            pygame.image.load("myndirnarb2/9.png").convert_alpha()
        )
        myndir["auka"] = (
            pygame.image.load("myndirnarb1/minus.png").convert_alpha(),
            pygame.image.load("myndirnarb1/milja.png").convert_alpha()
        )
        while True:
            # Mynd af bakgrunni
            myndir["bakgrunnur"] = pygame.image.load("myndirnarb1/DeutscheBank.png").convert()

            # Myndin af Bjögga
            myndir["leikmadur"] = (
                pygame.image.load("myndirnarb1/bjoggi-mynd.png").convert_alpha(),
            )

            # Myndirnar af peningum
            myndir["peningar"] = (
                pygame.image.load("myndirnarb1/500kr.png").convert_alpha(),
                pygame.image.load("myndirnarb1/1000kr.png").convert_alpha(),
                pygame.image.load("myndirnarb1/2000kr.png").convert_alpha(),
                pygame.image.load("myndirnarb1/5000kr.png").convert_alpha(),
                pygame.image.load("myndirnarb1/10000kr.png").convert_alpha(),
            )


            hreyfingar = self.Opnunargluggi()
            stada = -1200
            stada = self.leikur(hreyfingar, stada)
            return stada

def main():
    leikur= Bord1()
    leikur.keyrsla()

if __name__=="__main__":
    main()
