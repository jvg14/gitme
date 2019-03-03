from itertools import cycle
import random
import sys
import pygame
from pygame.locals import *

FPS = 30
breidd  = 576
haed = 512
sulubil  = 100 # Bilið á milli efri og neðri part súlunnar
# Vegalengdin sem grunnurinn getur farið til vinstri
grunnl = haed * 0.79
# Myndir, hljóð og hitmask dictionary
myndir, hljod, hitmask = {}, {}, {}

# Bakgrunnar
bakgrunnar = (
    "myndirnarb2/backg1.png",
    "myndirnarb2/backg2.png",
)

# Súlur
sulur = (
    "myndirnarb2/sulur1.png",
    "myndirnarb2/sulur2.png",
)

try:
    xrange
except NameError:
    xrange = range


class Bord2:
#Klasinn heldur utan um öll föllin sem notuð eru fyrir borð 2
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

        grunnurx = 0
        # Hámarkslengdin sem grunnurinn getur farið til vinstri
        grunnurfaersla = myndir["grunnur"].get_width() - myndir["bakgrunnur"].get_width()

        # LeikmadurVals fyrir upp og niður hreyfingar á valmyndinni
        leikmadurVals = {"val": 0, "dir": 1}

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    # Framkvæmi fyrstu hljóð og skila fyrir leikinn
                    hljod["wing"].play()
                    return {
                        "leikmadury": leikmadury + leikmadurVals["val"],
                        "grunnurx": grunnurx,
                        "leikmadurIndexGen": leikmadurIndexGen,
                    }

            # Lagfæra leikmadury, leikmadurIndex, grunnurx
            if (loopIter + 1) % 5 == 0:
                leikmadurIndex = next(leikmadurIndexGen)
            loopIter = (loopIter + 1) % 30
            grunnurx = -((-grunnurx + 4) % grunnurfaersla)
            self.leikmadurValmynd(leikmadurVals)

            # Teikna
            skjar.blit(myndir["bakgrunnur"], (0,0))
            skjar.blit(myndir["leikmadur"][0],
                        (leikmadurx, leikmadury + leikmadurVals["val"]))
            skjar.blit(myndir["skilabod"], (skilabodx, skilabody))
            skjar.blit(myndir["grunnur"], (grunnurx, grunnl))

            pygame.display.update()
            FPSCLOCK.tick(FPS)


    def leikur(self, hreyfingar):
        stada = leikmadurIndex = loopIter = 0
        leikmadurIndexGen = hreyfingar["leikmadurIndexGen"]
        leikmadurx, leikmadury = int(breidd * 0.2), hreyfingar["leikmadury"]

        grunnurx = hreyfingar["grunnurx"]
        grunnurfaersla = myndir["grunnur"].get_width() - myndir["bakgrunnur"].get_width()

        # Fæ 3 nýjar súlur og bæti í efrisulur og neðrisulur listana
        nysula1 = self.Random_Sula()
        nysula2 = self.Random_Sula()
        nysula3 = self.Random_Sula()

        # listi fyrir efri súlur
        efrisulur = [
            {"x": breidd + 200, "y": nysula1[0]["y"]},
            {"x": breidd + 200 + (breidd / 3), "y": nysula2[0]["y"]},
            {"x": breidd + 200 + (breidd * 2.0/3.0), "y": nysula3[0]["y"]},
        ]

        # listi fyrir neðri súlur
        nedrisulur = [
            {"x": breidd + 200, "y": nysula1[1]["y"]},
            {"x": breidd + 200 + (breidd / 3), "y": nysula2[1]["y"]},
            {"x": breidd + 200 + (breidd * 2.0/3.0), "y": nysula3[1]["y"]},
        ]

        # Hraði súla
        sulaVelX = -4

        # leikmaður hraði, hámarks hraði, hröðun niður, hröðun við space
        leikmadurVelY    =  -9   # Hraði leikmanns eftir Y-ás
        leikmadurMaxVelY =  10   # Hámarks hraði eftir Y-ás, hámarks fallhraði
        leikmadurMinVelY =  -8   # Minnsti hraði eftir Y-ás, hámarks hækkunar hraði
        leikmadurAccY    =   1   # Leikmanns hröðun niður
        leikmadurRot     =  45   # Snúningur leikmanns
        leikmadurVelRot  =   3   # Hornhraði
        leikmadurRotThr  =  20   # Snúnings þröskuldur
        leikmadurFlapAcc =  -9   # leikmanns hraði eftir hverja space-notkun
        leikmadurYtt = False # Satt þegar ýtt er á space


        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if leikmadury > -2 * myndir["leikmadur"][0].get_height():
                        leikmadurVelY = leikmadurFlapAcc
                        leikmadurYtt = True
                        hljod["wing"].play()

            # Ath. eftir árekstri
            arekst_prof = self.ath_arekstur({"x": leikmadurx, "y": leikmadury, "index": leikmadurIndex},
                                   efrisulur, nedrisulur)
            if arekst_prof[0]:
                return {
                    "y": leikmadury,
                    "grunn_arekst": arekst_prof[1],
                    "grunnurx": grunnurx,
                    "efrisulur": efrisulur,
                    "nedrisulur": nedrisulur,
                    "stada": stada,
                    "leikmadurVelY": leikmadurVelY,
                    "leikmadurRot": leikmadurRot
                }

            # Ath. stöðu
            leikmadurMidPos = leikmadurx + myndir["leikmadur"][0].get_width() / 2
            for sula in efrisulur:
                sulaMidPos = sula["x"] + myndir["sula"][0].get_width() / 2
                if sulaMidPos <= leikmadurMidPos < sulaMidPos + 4:
                    stada += 1
                    hljod["point"].play()

            # Breyta grunnurx með leikmadurIndex
            if (loopIter + 1) % 3 == 0:
                leikmadurIndex = next(leikmadurIndexGen)
            loopIter = (loopIter + 1) % 30
            grunnurx = -((-grunnurx + 100) % grunnurfaersla)

            # Snúa leikmanninum
            if leikmadurRot > -90:
                leikmadurRot -= leikmadurVelRot

            # Hreyfing leikmannsins
            if leikmadurVelY < leikmadurMaxVelY and not leikmadurYtt:
                leikmadurVelY += leikmadurAccY
            if leikmadurYtt:
                leikmadurYtt = False

                # Að snúa fyrir þröskuldinn
                leikmadurRot = 45

            leikmadurhaed = myndir["leikmadur"][0].get_height()
            leikmadury += min(leikmadurVelY, grunnl - leikmadury - leikmadurhaed)

            # Færa súlur til vinstri
            for esula, nsula in zip(efrisulur, nedrisulur):
                esula["x"] += sulaVelX
                nsula["x"] += sulaVelX

            # Bæta við nýrri súlu þegar fyrsta súlan snertir vinstri hlið
            if 0 < efrisulur[0]["x"] < 5:
                nysula = self.Random_Sula()
                efrisulur.append(nysula[0])
                nedrisulur.append(nysula[1])

            # Taka fyrstu súlu burt
            if efrisulur[0]["x"] < -myndir["sula"][0].get_width():
                efrisulur.pop(0)
                nedrisulur.pop(0)

            # Teikna
            skjar.blit(myndir["bakgrunnur"], (0,0))

            for esula, nsula in zip(efrisulur, nedrisulur):
                skjar.blit(myndir["sula"][0], (esula["x"], esula["y"]))
                skjar.blit(myndir["sula"][1], (nsula["x"], nsula["y"]))

            skjar.blit(myndir["grunnur"], (grunnurx, grunnl))

            # Sýni stöðuna í leiknum
            self.Syna_stodu(stada)

            # Snúningur leikmannsins hefur þröskuld.
            SynilegRot = leikmadurRotThr
            if leikmadurRot <= leikmadurRotThr:
                SynilegRot = leikmadurRot

            leikmaduryfirbord = pygame.transform.rotate(myndir["leikmadur"][0], SynilegRot)
            skjar.blit(leikmaduryfirbord, (leikmadurx, leikmadury))

            pygame.display.update()
            FPSCLOCK.tick(FPS)


    def Leik_lokid(self, arekstur):
        #Tekur leikmanninn og lætur hann detta
        stada = arekstur["stada"]
        leikmadurx = breidd * 0.2
        leikmadury = arekstur["y"]
        leikmadurhaed = myndir["leikmadur"][0].get_height()
        leikmadurVelY = arekstur["leikmadurVelY"]
        leikmadurAccY = 2
        leikmadurRot = arekstur["leikmadurRot"]
        leikmadurVelRot = 7

        grunnurx = arekstur["grunnurx"]

        efrisulur, nedrisulur = arekstur["efrisulur"], arekstur["nedrisulur"]

        # Spila hljóð fyrir árekstur
        hljod["hit"].play()
        if not arekstur["grunn_arekst"]:
            hljod["die"].play()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if leikmadury + leikmadurhaed >= grunnl - 1:
                        return

            # Færsla leikmanns á y-ás
            if leikmadury + leikmadurhaed < grunnl - 1:
                leikmadury += min(leikmadurVelY, grunnl - leikmadury - leikmadurhaed)

            # Breyta hraða leikmanns
            if leikmadurVelY < 15:
                leikmadurVelY += leikmadurAccY

            # Snúa þegar hann klessir á súlu
            if not arekstur["grunn_arekst"]:
                if leikmadurRot > -90:
                    leikmadurRot -= leikmadurVelRot

            # Teikna
            skjar.blit(myndir["bakgrunnur"], (0,0))

            for esula, nsula in zip(efrisulur, nedrisulur):
                skjar.blit(myndir["sula"][0], (esula["x"], esula["y"]))
                skjar.blit(myndir["sula"][1], (nsula["x"], nsula["y"]))

            skjar.blit(myndir["grunnur"], (grunnurx, grunnl))
            self.Syna_stodu(stada)

            leikmaduryfirbord = pygame.transform.rotate(myndir["leikmadur"][0], leikmadurRot)
            skjar.blit(leikmaduryfirbord, (leikmadurx,leikmadury))

            FPSCLOCK.tick(FPS)
            pygame.display.update()


    def leikmadurValmynd(self, leikmadurValmynd):
          # Lætur gildið af LeikmadurValmynd flakka á milli -8 og 8
        if abs(leikmadurValmynd["val"]) == 8:
            leikmadurValmynd["dir"] *= -1

        if leikmadurValmynd["dir"] == 1:
             leikmadurValmynd["val"] += 1
        else:
            leikmadurValmynd["val"] -= 1


    def Random_Sula(self):
          # Skilar randomly gerðri súlu
        # Hæðar munur á efri og neðri súlu
        gapY = random.randrange(0, int(grunnl * 0.6 - sulubil))
        gapY += int(grunnl * 0.2)
        sulaHeight = myndir["sula"][0].get_height()
        sulaX = breidd + 10

        return [
            {"x": sulaX, "y": gapY - sulaHeight},  # efri súla
            {"x": sulaX, "y": gapY + sulubil}, # neðri súla
        ]


    def Syna_stodu(self, stada):
        # Sýni stöðu í miðjum skjánum
        stadaDigits = [int(x) for x in list(str(stada))]
        totalWidth = 0 # Heildar breidd af öllum númerum sem verða prentuð

        for digit in stadaDigits:
            totalWidth += myndir["numer"][digit].get_width()

        Xoffset = (breidd - totalWidth) / 2

        for digit in stadaDigits:
            skjar.blit(myndir["numer"][digit], (Xoffset, haed * 0.1))
            Xoffset += myndir["numer"][digit].get_width()


    def ath_arekstur(self, leikmadur, efrisulur, nedrisulur):
        # Skila true ef árekstur verður á milli leikmanns og grunns eða súla
        pi = leikmadur["index"]
        leikmadur["w"] = myndir["leikmadur"][0].get_width()
        leikmadur["h"] = myndir["leikmadur"][0].get_height()

        # Ef leikmaður lendur á jörðinni
        if leikmadur["y"] + leikmadur["h"] >= grunnl - 1:
            return [True, True]
        else:
            leikmadurhnit = pygame.Rect(leikmadur["x"], leikmadur["y"],
                          leikmadur["w"], leikmadur["h"])
            sulaW = myndir["sula"][0].get_width()
            sulaH = myndir["sula"][0].get_height()

            for esula, nsula in zip(efrisulur, nedrisulur):
                # Efri og neðri súlu hnit
                esuluhnit = pygame.Rect(esula["x"], esula["y"], sulaW, sulaH)
                nsuluhnit = pygame.Rect(nsula["x"], nsula["y"], sulaW, sulaH)

                # Leikmanns, efri og neðri súlu hitmask
                lHitmask = hitmask["leikmadur"][0]
                eHitmask = hitmask["sula"][0]
                nHitmask = hitmask["sula"][1]

                # Hvort árekstur verður við efri eða neðri súlu
                efri_arekstur = self.Pixel_Arekstur(leikmadurhnit, esuluhnit, lHitmask, eHitmask)
                nedri_arekstur = self.Pixel_Arekstur(leikmadurhnit, nsuluhnit, lHitmask, nHitmask)

                if efri_arekstur or nedri_arekstur:
                    return [True, False]

        return [False, False]

    def Pixel_Arekstur(self, hnit1, hnit2, hitmask1, hitmask2):
        #Ath. hvort tveir hlutir klessa á hvorn annan
        hnit = hnit1.clip(hnit2)

        if hnit.width == 0 or hnit.height == 0:
            return False

        x1, y1 = hnit.x - hnit1.x, hnit.y - hnit1.y
        x2, y2 = hnit.x - hnit2.x, hnit.y - hnit2.y

        for x in xrange(hnit.width):
            for y in xrange(hnit.height):
                if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                    return True
        return False

    def Saekja_Hitmask(self, image):
        # Skilar hitmask
        mask = []
        for x in xrange(image.get_width()):
            mask.append([])
            for y in xrange(image.get_height()):
                mask[x].append(bool(image.get_at((x,y))[3]))
        return mask

    def keyrsla(self):
        global skjar, FPSCLOCK
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        skjar = pygame.display.set_mode((breidd, haed))
        pygame.display.set_caption("Borð 2")

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

        # Myndin fyrir opnunargluggan
        myndir["skilabod"] = pygame.image.load("myndirnarb2/message1.png").convert_alpha()
        # Grunnurinn fyrir borðið
        myndir["grunnur"] = pygame.image.load("myndirnarb2/grunnur1.png").convert_alpha()

        # Hljóðið
        if "win" in sys.platform:
            HljodExt = ".wav"
        else:
            HljodExt = ".ogg"

        hljod["die"]    = pygame.mixer.Sound("hljodinb2/die" + HljodExt)
        hljod["hit"]    = pygame.mixer.Sound("hljodinb2/hit" + HljodExt)
        hljod["point"]  = pygame.mixer.Sound("hljodinb2/point" + HljodExt)
        hljod["swoosh"] = pygame.mixer.Sound("hljodinb2/swoosh" + HljodExt)
        hljod["wing"]   = pygame.mixer.Sound("hljodinb2/wing" + HljodExt)

        while True:
            # Vel random bakgrunn
            randBg = random.randint(0, len(bakgrunnar) - 1)
            myndir["bakgrunnur"] = pygame.image.load(bakgrunnar[randBg]).convert()

            # Myndin af Bjögga
            myndir["leikmadur"] = (
                pygame.image.load("myndirnarb2/bjoggi-mynd.png").convert_alpha(),
            )

            # Vel random súlur
            sulaindex = random.randint(0, len( sulur) - 1)
            myndir["sula"] = (
                pygame.transform.rotate(
                    pygame.image.load(sulur[sulaindex]).convert_alpha(), 180),
                pygame.image.load(sulur[sulaindex]).convert_alpha(),
            )

            # Hitmask for súlurnar
            hitmask["sula"] = (
                self.Saekja_Hitmask(myndir["sula"][0]),
                self.Saekja_Hitmask(myndir["sula"][1]),
            )

            # Hitmask fyrir leikmanninn
            hitmask["leikmadur"] = (
                self.Saekja_Hitmask(myndir["leikmadur"][0]),
            )

            hreyfingar = self.Opnunargluggi()
            arekstur = self.leikur(hreyfingar)
            self.Leik_lokid(arekstur)

def main():
    leikur = Bord2()
    leikur.keyrsla()

if __name__=="__main__":
    main()
