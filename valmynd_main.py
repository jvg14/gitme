
import pygame
from pygame import *


pygame.init()

skjar = pygame.display.set_mode((576, 512)) #576 512
timi = pygame.time.Clock()

SVARTUR = (0, 0, 0)
HVITUR = (255, 255, 255)
HOVER_COLOR = (50, 70, 90)

#tonlist
pygame.mixer.music.load('sound.ogg')
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play()
pygame.display.update()
timi.tick(15)

#bakgrunnsmynd
bakgrunnur = pygame.image.load("btb_valmynd_cartoon.png")

#letur
LETUR = pygame.font.SysFont ("Calibri", 50)
minna_letur = pygame.font.SysFont ("Calibri", 30)


texti1 = LETUR.render("BYRJA", True, HVITUR)
texti2 = LETUR.render("LÝSING", True, HVITUR)
texti3 = LETUR.render("UM LEIKINN", True, HVITUR)
texti4 = LETUR.render("BYRJA LEIK", True, HVITUR)

#flytileidir
kassi1 = pygame.Rect(50,400,115,35)
kassi2 = pygame.Rect(200,400,130,35)
kassi3 = pygame.Rect(350,400,205,35)
kassi4 = pygame.Rect(350,400,205,35)

takkar = [
    [texti1, kassi1, SVARTUR],
    [texti2, kassi2, SVARTUR],
    [texti3, kassi3, SVARTUR]
    ]

running = False

def um_leikinn():

    pygame.display.set_caption('Um leikinn')
    skjar.blit(bakgrunnur,(0,0))

    texti_umleikinn = pygame.image.load("texti_umleikinn1.png")
    skjar.blit(texti_umleikinn,(20,20))

    pygame.display.flip()

    while 1:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                break
            elif event.key == pygame.K_UP:
                game_intro()
        pygame.display.flip()

def byrja_uppl():
    pygame.display.set_caption('Lýsing á leiknum')
    skjar.blit(bakgrunnur,(0,0))

    lysing = pygame.image.load("lysing.png")
    skjar.blit(lysing,(70,20))

    bord1 = pygame.image.load("bord1.png")
    skjar.blit(bord1,(60,350))

    bord2 = pygame.image.load("bord2.png")
    skjar.blit(bord2,(180,350))

    bord3= pygame.image.load("bord3.png")
    skjar.blit(bord3,(300,350))

    bord4 = pygame.image.load("bord4.png")
    skjar.blit(bord4,(420,350))

    pygame.display.flip()



def game_intro():

    pygame.display.set_caption('Valmynd')

    while not running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEMOTION:
                for takki in takkar:
                    if takki[1].collidepoint(event.pos):
                        takki[2] = HOVER_COLOR
                    else:
                        takki[2] = SVARTUR

                        skjar.blit(bakgrunnur, (0, 0))
            for texti, kassi, litur in takkar:
                pygame.draw.rect(skjar, litur, kassi)
                skjar.blit(texti, kassi)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if kassi1.collidepoint(event.pos):
                            byrja_uppl()
                        elif kassi2.collidepoint(event.pos):
                            print ('lysing')
                        elif kassi3.collidepoint(event.pos):
                            um_leikinn()

                pygame.display.flip()
                timi.tick(60)

def main():
    game_intro()
    pygame.quit()

if __name__=="__main__":
    main()
