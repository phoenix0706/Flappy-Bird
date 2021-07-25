import random #For generating random numbers
import sys #to use sys.exit in order to exit the program
import pygame
from pygame.locals import * #Basic pygame imports



#Global Variables for the game
fps=32 #frames per sec
Screen_Width=289
Screen_Height=511
Game_sprites={} #dictionary 
Game_Sounds={}
Player="img/bird.png" 
Background="img/bg_city.png"
Pipe="img/pipe.png"

#Screen of game
Screen=pygame.display.set_mode((Screen_Width,Screen_Height))
Ground_y=Screen_Height*0.8






def welcomeScreen():
    playerx=int(Screen_Width/5)
    playery=int((Screen_Height-Game_sprites['player'].get_height())/2)
    messagex=int((Screen_Width-Game_sprites['message'].get_width())/2)
    messagey=int(Screen_Height*0.13)
    basex=0
    while True:
        for event in pygame.event.get():
         #if user clicks close button
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            #user starts the game
            elif event.type==KEYDOWN and(event.key==K_SPACE or event.key==K_UP):
                return

            
            else:
                Screen.blit(Game_sprites['background'],(0,0))
                Screen.blit(Game_sprites['player'],(playerx,playery))
                Screen.blit(Game_sprites['message'],(messagex,messagey))
                Screen.blit(Game_sprites['base'],(basex,Ground_y))
                pygame.display.update()
                fpsclock.tick(fps)





def mainGame():
    score=0
    playerx=int(Screen_Width/5)
    playery=int(Screen_Width/2)
    basex=0

    #creating pipes
    newpipe1=getRandomPipe()
    newpipe2=getRandomPipe()

    #making lists of upper and lower pipe
    upperPipes=[
        {'x':Screen_Width+200,'y':newpipe1[0]['y']},
        {'x':Screen_Width+200+(Screen_Width/2),'y':newpipe2[0]['y']}
          ]
    lowerPipes=[
        {'x':Screen_Width+200,'y':newpipe1[1]['y']},
        {'x':Screen_Width+200+(Screen_Width/2),'y':newpipe2[1]['y']}
          ]
    pipevelx=-4
    playervely=-9
    playerminvely=-8
    playermaxvely=10
    playerAccy=1



    playerflapaccv=-8 #velocity while flapping
    playerflapped=False #true only when bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playervely=playerflapaccv
                    playerflapped=True
                    Game_Sounds['wing'].play()
        
        crashTest=isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            return
            

        
        #check score
        playermidpos=playerx+Game_sprites['player'].get_width()/2
        for pipe in upperPipes:
            pipemidpos=pipe['x']+Game_sprites['pipe'][0].get_width()/2
            if pipemidpos<= playermidpos< pipemidpos+4:
                score+=1
                #print(f"Your score is {score}" )
                Game_Sounds['point'].play()

        
        if playervely<playermaxvely and not playerflapped:
            playervely+=playerAccy

        if playerflapped:
            playerflapped=False
        
        playerheight=Game_sprites['player'].get_height()
        playery=playery+min(playervely,Ground_y-playery-playerheight)

        
        #move pipes to the left
        for upperpipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperpipe['x']+=pipevelx
            lowerPipe['x']+=pipevelx

        #adding a new pipe before removing leftmost pipe
        if 0<upperPipes[0]['x']<5:
            newpipe=getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])




        #if the pipe is out of screen, remove it
        if upperPipes[0]['x']< -Game_sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)



       

        #blitting our sprites
        Screen.blit(Game_sprites['background'],(0,0))
        for upperpipe,lowerPipe in zip(upperPipes,lowerPipes):
            Screen.blit(Game_sprites['pipe'][0],(upperpipe['x'],upperpipe['y']))
            Screen.blit(Game_sprites['pipe'][1],(lowerPipe['x'],lowerPipe['y']))


        Screen.blit(Game_sprites['base'],(basex,Ground_y))
        Screen.blit(Game_sprites['player'],(playerx,playery))
        myDigits=[int(x) for x in list(str(score))]
        width=0
        for digit in myDigits:
            width+=Game_sprites['numbers'][digit].get_width()
        Xoffset=(Screen_Width-width)/2

        for digit in myDigits:
            Screen.blit(Game_sprites['numbers'][digit],(Xoffset,Screen_Height*0.12))
            Xoffset+=Game_sprites['numbers'][digit].get_width()
        pygame.display.update()
        fpsclock.tick(fps)





def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery > Ground_y-25 or playery < 0:
        Game_Sounds['hit'].play()
        return True
        
    for pipe in upperPipes:
        pipeHeight=Game_sprites['pipe'][0].get_height()
        if (playery<pipeHeight+pipe['y']and abs(playerx-pipe['x'])<Game_sprites['pipe'][0].get_width()):
            Game_Sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery+Game_sprites['player'].get_height()>pipe['y']) and abs(playerx-pipe['x'])<Game_sprites['pipe'][0].get_width():
            Game_Sounds['hit'].play()
            return True

    return False

            





def getRandomPipe():
    pipeheight=Game_sprites['pipe'][0].get_height()
    offset=Screen_Height/3
    y2=offset+random.randrange(0,int(Screen_Height-Game_sprites['base'].get_height()-1.2*offset))
    pipeX=Screen_Width+10
    y1=pipeheight-y2+offset
    pipe=[
        {'x':pipeX,'y':-y1}, #upper pipe
        {'x':pipeX,'y':y2} #lower pipe
    ]
    return pipe


if __name__=="__main__":
    #game starts from here
    pygame.init() #initializes all pygame's modules

    fpsclock=pygame.time.Clock() #controls fps in game
    
    pygame.display.set_caption('Flappy Bird by Phoenix')
    Game_sprites['numbers'] = ( 
        pygame.image.load('img/0.png').convert_alpha(),
        pygame.image.load('img/1.png').convert_alpha(),
        pygame.image.load('img/2.png').convert_alpha(),
        pygame.image.load('img/3.png').convert_alpha(),
        pygame.image.load('img/4.png').convert_alpha(),
        pygame.image.load('img/5.png').convert_alpha(),
        pygame.image.load('img/6.png').convert_alpha(),
        pygame.image.load('img/7.png').convert_alpha(),
        pygame.image.load('img/8.png').convert_alpha(),
        pygame.image.load('img/9.png').convert_alpha(),
    )

    Game_sprites['message'] =pygame.image.load('img/introscreen.png').convert_alpha()
    Game_sprites['base'] =pygame.image.load('img/base.png').convert_alpha()
    Game_sprites['pipe'] =(pygame.transform.rotate(pygame.image.load( Pipe).convert_alpha(), 180), 
    pygame.image.load(Pipe).convert_alpha()
    )

    # Game sounds
    Game_Sounds['die'] = pygame.mixer.Sound('audio/die.wav')
    Game_Sounds['hit'] = pygame.mixer.Sound('audio/hit.wav')
    Game_Sounds['point'] = pygame.mixer.Sound('audio/point.wav')
    Game_Sounds['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    Game_Sounds['wing'] = pygame.mixer.Sound('audio/wing.wav')

    Game_sprites['background'] = pygame.image.load(Background).convert()
    Game_sprites['player'] = pygame.image.load(Player).convert_alpha()
    

            
    while(True):
        welcomeScreen() #shows welcome screen to user until he/she presses any key or button
        mainGame()  #this is maingame functions
        welcomeScreen()
       

    




