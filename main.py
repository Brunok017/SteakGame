import pygame
import os
import sys
import random
import math
import subprocess
import sqlite3
from pygame.locals import *

pygame.init()

#Colors
white= (255, 255, 255)
black=(0,0,0,0)
red=(255, 0, 0)
gold=(240,230,170)
blue=(0,190,255)

#Fonts
Big_font = pygame.font.Font("freesansbold.ttf", 40)
Lose_Font = pygame.font.Font("freesansbold.ttf", 80)

#Sprites
steak = pygame.image.load('.\imgs\steak.png')
knifesprite = pygame.image.load('.\imgs\knife.png')
background = pygame.image.load(".\imgs\Background.png")
speedup = pygame.image.load(".\imgs\speed.png")
losescreen = pygame.image.load(".\imgs\lose.png")
playbutton = pygame.image.load(".\imgs\playbut.png")
quitbutton = pygame.image.load(".\imgs\quitbut.png")


#Window
clock = pygame.time.Clock()
winw, winh = 600, 600
win = pygame.display.set_mode((winw, winh))
pygame.display.set_caption("High Steaks")

#Vars
score=0
mod=True
Buffout=False
Playermod = True
speed=6
xsize = 20.5
ysize= 84.5
newscore = 0
newknife = None
newBuff = None
lose = False
pausecheck=False
changevalx = 0
changevaly = 0
highscore = 0

#Database
conn = sqlite3.connect('Game.db')
cursor = conn.cursor()
sql='''CREATE TABLE IF NOT EXISTS GameTable (RecentScore INTEGER, Highscore INTEGER, KnifeCount INTEGER)'''
cursor.execute(sql)



#Classes
#Each pygame class that says pygame.sprite.Sprite has a built in draw function!!!!
class Player():
    def __init__(self, color, x, y, width, height, pspeed):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pspeed = pspeed

    #This is how I display the player hitbox and sprite
    def disp(self, win, color, name):
        if lose == False:
            pygame.draw.rect(win, color, name)
            win.blit(steak, ((player.x-27),(player.y-29)))

    #This is the movement for the player which 
    #links to the event handler in the bottom run loop
    def move(self):
        player.x += changevalx
        player.y += changevaly
        if player.x > (winw-50):
            player.x = (winw-50)
        elif player.x < 0:
            player.x = 0
        elif player.y >= (winh-50):
            player.y = (winh-50)
        elif player.y < 0:
            player.y = 0
    
        
#Instances for player
player1 = Player(white,300,500,34,34,3) 
player = pygame.Rect(player1.x,player1.y,player1.width,player1.height)


#When the score hits 25 there is a box that comes out
#If the player hits this it will decrease the knife speed by 1
class Buff(pygame.sprite.Sprite):
    def __init__(self, color, x, y, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.speedx = speedx
        self.speedy = speedy

#Movement and display for buff
    def update(self):
        global Buffout
        if round(score) % 25 == 0 and score !=0:
            Buffout = True
        if Buffout == True:
            win.blit(speedup, (self.rect.centerx-25,self.rect.centery-25))
            print("buff")
            self.rect.move_ip(self.speedx,self.speedy)
            if self.rect.right == 600:
                self.speedx *= -1
            elif self.rect.left == 0:
                self.speedx *= -1
            elif self.rect.centery == 600:
                self.speedy *= -1
            elif self.rect.top == 0:
                self.speedy *= -1
            
            
            
    #Collisons for Buff
    def col(self):
        global Buffout
        global Playermod
        global speed
        if player.colliderect(self.rect) and Playermod == True:
            speed -= 1
            Playermod = False
            self.kill()

#Instances for Buff
newBuff = Buff(blue,20,20,1,1)
Buffs = pygame.sprite.Group()
Buffs.add(newBuff)

#Knives
class Knife(pygame.sprite.Sprite):
    def __init__(self, color, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((xsize, ysize))
        self.image.fill(color)
        self.rect= self.image.get_rect()
        self.rect.center = (x,y)
        self.speed = speed

    #Movement for knives and score processing
    def update(self):
        global score
        global newscore
        self.rect.move_ip(0,speed)
        if self.rect.top > 600:
            self.rect.top = -160
            self.rect.centerx=random.randint(1,570)
            if len(knives) == 1:
                score+=1
            if len(knives) > 1:
                score+=(1/len(knives))

    #Added effects for knives
    #Size increase does not work yet!
    #I'm taking it out
    def alter(self):
        global mod
        global speed
        global xsize
        global ysize
        global newknife
        if round(score) % 5 == 0 and score !=0:
            modification = random.randint(1,2)
            if modification == 1 and mod==True:
                print("speed up")
                speed += 1
                mod=False
            elif modification ==3 and mod==True:
                print("SizeUp")
                xsize +=15
                ysize += 45
                mod=False
            elif modification ==2 and mod==True:
                print("New Knife")
                newknife = Knife(white,random.randint(1,570),0,5)
                knives.add(newknife)
                mod=False
        elif score % 5 !=0:
            mod = True

    #knife collision
    def col(self):
        global run
        global newknife
        global lose
        if player.colliderect(self.rect):
            lose = True

    #knife sprites
    def spriteblit(self):
        win.blit(knifesprite,((self.rect.centerx-130),(self.rect.centery-130)))    


#Knife Instances
knives = pygame.sprite.Group()
            
knife = Knife(white,random.randint(1,570),0,5)
knives.add(knife)       

#Buttons for lose menu
class Button():
    def __init__(self, x,y, image, purpose):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    #Start button code
    def start(self):    
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                subprocess.run(['python', 'main.py'])
                sys.exit()
    
    #Quit button code
    def quit(self):    
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                sys.exit()


        
#ButtonInstances
playbutt = Button(200, 410, playbutton, "start")
quitbutt = Button(200, 485, quitbutton, "quit")

#global functions

#Displaying score
def scoreblit():
    if lose == False:
        win.blit(scoreyshad,(302.5,13))
        win.blit(scorey,(300,10))
    elif lose == True:
        win.blit(scoreyshad,(282.5,200))
        win.blit(scorey,(280,200))
        win.blit(HighFontshad,(282.5,360))
        win.blit(HighFont,(280,360))

#Displaying Lose Menu
def game_over():
    global speed
    global changevaly
    global changevalx
    if lose == True:
        speed = 0
        win.blit(losescreen,(150,100))
        playbutt.draw()
        quitbutt.draw()
        playbutt.start()
        quitbutt.quit()

#Did not get to pause         
def pause():
    global speed
    if pausecheck==True:
        speed=0
        player1.pspeed=0

#RunLoop
#This is how pygame runs
run=True
while run:
    #Ticks every 10 mili seconds and updates the screen
    pygame.time.delay(10)

    #This is the mentioned Event Handler, 
    #It handles input with the arrow keys
    #I know it looks rough
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN and lose==False:
            if event.key == pygame.K_RIGHT:
                changevalx += player1.pspeed
            elif event.key == pygame.K_LEFT:
                changevalx -= player1.pspeed
            elif event.key == pygame.K_UP:
                changevaly -= player1.pspeed
            elif event.key == pygame.K_DOWN:
                changevaly += player1.pspeed
        elif event.type == pygame.KEYUP and lose==False:
            if event.key == pygame.K_RIGHT:
                changevalx -= player1.pspeed
            elif event.key == pygame.K_LEFT:
                changevalx += player1.pspeed
            elif event.key == pygame.K_UP:
                changevaly += player1.pspeed
            elif event.key == pygame.K_DOWN:
                changevaly -= player1.pspeed
           
            
                
    #This is calling the functions in the run loop            
    win.blit(background, (0,0))
    scoreyshad = Big_font.render(f'{round(score)}', True, black)
    scorey = Big_font.render(f'{round(score)}', True, white)
    LoseFont = Lose_Font.render(f'{"You Lose"}', True, red)
    HighFontshad = Big_font.render(f'{highscore}', True, black)
    HighFont = Big_font.render(f'{highscore}', True, white)

    player1.move()
    knives.update()
    knives.draw(win)
    Buffs.update()
    Buffs.draw(win)
    
    player1.disp(win, white, player)
    player1.move()
    knife.alter()
    knife.col()
    knife.spriteblit()
    #These are because the sprite groups start out null
    if newknife:
        for newknife in knives:
            newknife.col()
            newknife.spriteblit()
            newknife.alter()
    if newBuff:
        for newBuff in Buffs:
            Buffs.draw(win)
            newBuff.update()
            newBuff.col()
    game_over()
    scoreblit()
    
    
    
    
    
    #Last of the pygame window setup
    pygame.display.update()
    clock.tick(60)
    win.fill(black)
pygame.quit()
os.system('cls')
sys.exit()