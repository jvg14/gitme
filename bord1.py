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


def Opnunargluggi():
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
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # Framkvæmi fyrstu hljóð og skila fyrir leikinn
                return {
                    "leikmadury": leikmadury + leikmadurVals["val"],
                    "leikmadurIndexGen": leikmadurIndexGen,
                }

        # Lagfæra leikmadury, leikmadurIndex
        if (loopIter + 1) % 5 == 0:
            leikmadurIndex = next(leikmadurIndexGen)
        loopIter = (loopIter + 1) % 30
        leikmadurValmynd(leikmadurVals)

        # Teikna
        skjar.blit(myndir["bakgrunnur"], (0,0))
        skjar.blit(myndir["leikmadur"][0],
                    (leikmadurx, leikmadury + leikmadurVals["val"]))
        skjar.blit(myndir["skilabod"], (skilabodx, skilabody))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def leikur(hreyfingar):
    # Fæ random staðsetningu á pening
    nyrpeningur1 = Random_Peningur()

    # Listi fyrir peninga
    Peningar = [
        {"z": nyrpeningur1[0]["z"], "x": nyrpeningur1[0]["x"], "y": nyrpeningur1[0]["y"]},
    ]
    time_elapsed_since_last_action = 0
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                pass

        dt = clock.tick()
        time_elapsed_since_last_action += dt
        if time_elapsed_since_last_action > 2500:
            nyrpeningur = Random_Peningur()
            Peningar.append(nyrpeningur[0])
            time_elapsed_since_last_action = 0

        # Teikna
        skjar.blit(myndir["bakgrunnur"], (0,0))
        for nyrpeningur1 in Peningar:
            # Vel random pening
            randpen = random.randint(0, 4)
            skjar.blit(myndir["peningar"][nyrpeningur1["z"]], (nyrpeningur1["x"], nyrpeningur1["y"]))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def Saekja_Hitmask(image): # Sama fall og borð 2 notar
    # Skilar hitmask
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask


def leikmadurValmynd(leikmadurValmynd): # Sama fall og borð 2 notar
      # Lætur gildið af LeikmadurValmynd flakka á milli -8 og 8
    if abs(leikmadurValmynd["val"]) == 8:
        leikmadurValmynd["dir"] *= -1

    if leikmadurValmynd["dir"] == 1:
         leikmadurValmynd["val"] += 1
    else:
        leikmadurValmynd["val"] -= 1

def Random_Peningur():
    # Skilar random pening
    # Staðsetning penings
    Stad_x = random.randint(50, breidd-50)
    Stad_y = random.randint(23, haed-23)
    Mynd = random.randint(0, 4)
    return [
        {"z": Mynd ,"x": Stad_x, "y": Stad_y},
    ]

def main():
    global skjar, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    skjar = pygame.display.set_mode((breidd, haed))
    pygame.display.set_caption("Borð 1")


    # Myndin fyrir opnunargluggan
    myndir["skilabod"] = pygame.image.load("myndirnarb1/Valmynd.png").convert_alpha()

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


        hreyfingar = Opnunargluggi()
        leikur(hreyfingar)

if __name__=="__main__":
    main()
