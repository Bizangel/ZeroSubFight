import pygame
import Modules.extraFunctions as extra
from math import radians,cos,sin

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
MAPHEIGHT = 896
GAMEWIDTH = 1280
GAMEHEIGHT = 964
class Hazard:
    Hazards = []
    def __init__(self,x,y,xvel,yvel,asset):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.asset = asset
        self.rect = pygame.Rect(self.x,self.y,23,32)
        self.animIndex = 0
        Hazard.Hazards.append(self)
    def update(self,player1,player2,tileHitbox):
        self.rect.top -= self.yvel
        self.rect.left += self.xvel
        self.animIndex +=1
        if self.animIndex >11: self.animIndex = 0
        self.collide(player1,player2,tileHitbox)
        
    def delete(self):
        deleter = Hazard.Hazards.index(self)
        del Hazard.Hazards[deleter]
        
    def draw(self,displaysurf):
        displaysurf.blit(self.asset,self.rect,((self.animIndex//4)*23,0,23,32))

    def collide(self,player1,player2,tileHitbox):
        if self.rect.colliderect(player1.rect):
            player1.hp -= 30
            if player1.hp < 0: player1.hp = 0
            self.delete()
            player1.hit = True

        elif self.rect.colliderect(player2.rect):
            player2.hp -= 30
            if player2.hp < 0: player2.hp = 0
            player2.hit = True
            self.delete()
        else:
            if self.rect.collidelist(tileHitbox) != -1:
                #collided
                self.delete()
            
        
        
class SmallParticles:
    Particles = []
    def __init__(self,x,y,playertrack,asset):
        self.x = x
        self.y = y
        self.playertrack = playertrack
        self.asset = asset
        if self.asset == 'lifedrain': self.hpeffect = 2
        self.rect = pygame.Rect(x,y,3,3)
        self.timer = 0
        SmallParticles.Particles.append(self)
    def update(self,player1,player2):
        if self.playertrack == 'player1': playertrack = player1
        else: playertrack = player2
        self.timer += 1
        angle = extra.pointToAngle((self.rect.centerx,self.rect.centery),(playertrack.rect.centerx,playertrack.rect.centery),False)
        self.rect.left += cos(radians(angle))*15
        self.rect.top += sin(radians(angle))*15
        self.collide(playertrack)
                

    def collide(self,playertrack):
        if self.asset == 'lifedrain':
            if self.rect.colliderect(playertrack.rect):
                playertrack.hp += self.hpeffect
                if playertrack.hp > 300: playertrack.hp = 300
                self.delete()

    def draw(self,displaysurf):
        if self.asset == 'lifedrain': pygame.draw.circle(displaysurf,RED,(self.rect.left,self.rect.top),3)
            
    def delete(self):
        deleter = SmallParticles.Particles.index(self)
        del SmallParticles.Particles[deleter]
        
        
 
def DrawHUD(displaysurf,HUDAssets,chipAssets,Texts,PlayerInfo):
    '''Receives a surface the HUD assets, the hp texts and a list of tuples,PlayerInformation containing
    the player CD Timer and Health of each player, to draw everything properly'''
    hp1,nadecd1,overheat1,weapon1,weptimer1,wins1 =PlayerInfo[0]
    hp2,nadecd2,overheat2,weapon2,weptimer2,wins2 = PlayerInfo[1]
    #texts[2 and 3] are playerwins

    pygame.draw.rect(displaysurf,BLACK,(0,MAPHEIGHT,GAMEWIDTH,GAMEHEIGHT-MAPHEIGHT)) #Clears everything with black rect
    #color degrade for Line and circle
    overColor1 = (255,255-(overheat1*255/1000),0)
    overColor2 = (255,255-(overheat2*255/1000),0)
    angle1 = radians(180-overheat1*180/1000)
    angle2 = radians(180-overheat2*180/1000)
    #Draw Overheat Meters
    pygame.draw.circle(displaysurf,overColor1,(200,MAPHEIGHT+40),30,2)
    pygame.draw.circle(displaysurf,overColor2,(GAMEWIDTH-200,MAPHEIGHT+40),30,2)
    
    pygame.draw.rect(displaysurf,BLACK,(0,MAPHEIGHT+40,GAMEWIDTH,GAMEHEIGHT-MAPHEIGHT))
    
    pygame.draw.line(displaysurf,overColor1,(170,MAPHEIGHT+40),(230,MAPHEIGHT+40),2)
    pygame.draw.line(displaysurf,overColor2,(GAMEWIDTH-170,MAPHEIGHT+40),(GAMEWIDTH-230,MAPHEIGHT+40),2)
    
    pygame.draw.line(displaysurf,RED,(200,MAPHEIGHT+40),(200+cos(angle1)*30, MAPHEIGHT+40-sin(angle1)*30),2   )
    pygame.draw.line(displaysurf,RED,(GAMEWIDTH-200,MAPHEIGHT+40),(GAMEWIDTH-200+cos(angle2)*30, MAPHEIGHT+40-sin(angle2)*30 ),2)
    displaysurf.blit(HUDAssets[1],(0,MAPHEIGHT+15))
    
    #Draws HP bar and draws rect over hp
    displaysurf.blit(HUDAssets[2],(60,MAPHEIGHT+20),(0,0,hp1*(1/3),11))
    displaysurf.blit(HUDAssets[3],(60,MAPHEIGHT+20))
    displaysurf.blit(Texts[0],(60,MAPHEIGHT+30))
    #Draws NadeBar
    displaysurf.blit(HUDAssets[4],(30,MAPHEIGHT+45),(0,0,nadecd1*(89/600)-1,11))
    displaysurf.blit(HUDAssets[5],(30,MAPHEIGHT+45))
    #Player2 Hud
    displaysurf.blit(HUDAssets[6],(GAMEWIDTH-52,MAPHEIGHT+15))
    displaysurf.blit(HUDAssets[7],(GAMEWIDTH-160,MAPHEIGHT+20),(0,0,hp2*(1/3),11))
    displaysurf.blit(HUDAssets[3],(GAMEWIDTH-160,MAPHEIGHT+20))
    displaysurf.blit(Texts[1],(GAMEWIDTH-160,MAPHEIGHT+30))
    #Nadebar
    displaysurf.blit(HUDAssets[8],(GAMEWIDTH-105,MAPHEIGHT+45),(0,0,nadecd2*(89/600)-1,15))
    displaysurf.blit(HUDAssets[9],(GAMEWIDTH-105,MAPHEIGHT+45))
    #Draw HUDGuns
    adjustx1,adjusty1,adjustx2,adjusty2 = 0,0,0,0
    if weapon1 == 2: adjustx1,adjusty1 = -5, -10
    if weapon2 == 2: adjustx2,adjusty2 = 20, -10
    
    if weapon1 == 3: adjustx1,adjusty1 = -5, -10
    if weapon2 == 3: adjustx2,adjusty2 = 30, -10

    if weapon1 == 4: adjustx1,adjusty1 = 0,-5
    if weapon2 == 4: adjustx2,adjusty2 = 10,-5
    
    displaysurf.blit(HUDAssets[12],(170,MAPHEIGHT+50))
    displaysurf.blit(HUDAssets[13],(GAMEWIDTH-220,MAPHEIGHT+50))
    #Draw chips
    if weapon1 != 0:
        displaysurf.blit(chipAssets[weapon1],(240,MAPHEIGHT+15),(0,0,30,30- (weptimer1*30/720) ) ) 
        
        displaysurf.blit(HUDAssets[15][weapon1],(230+adjustx1,MAPHEIGHT+54+adjusty1)) #Draws current weapon Icon
    else: displaysurf.blit(HUDAssets[10],(225,MAPHEIGHT+45))
    
    if weapon2 != 0:
        displaysurf.blit(chipAssets[weapon2],(GAMEWIDTH-270,MAPHEIGHT+15),(0,0,30,30- (weptimer2*30/720) ) )
        
        displaysurf.blit(HUDAssets[15][weapon2],(GAMEWIDTH-265+adjustx2,MAPHEIGHT+54+adjusty2)) #Draws current weapon Icon
    else: displaysurf.blit(HUDAssets[11],(GAMEWIDTH-243,MAPHEIGHT+45))



    #Draw Crowns and player wins
    if wins1 > 0 or wins2 > 0: #If wins are more than 0, draw win counter
        displaysurf.blit(Texts[2], (150,GAMEHEIGHT-20))
        displaysurf.blit(Texts[3], (GAMEWIDTH-135,GAMEHEIGHT-20))
        #Draw stars
        displaysurf.blit(HUDAssets[14],(130,GAMEHEIGHT-20))
        displaysurf.blit(HUDAssets[14],(GAMEWIDTH-150,GAMEHEIGHT-20))
        
        #Draw Win Crown on who ever has more wins atm.
        if wins1 > wins2: displaysurf.blit(HUDAssets[0],(22,MAPHEIGHT+2))
        elif wins2 > wins1: displaysurf.blit(HUDAssets[0],(GAMEWIDTH-35,MAPHEIGHT+2))
    #If the wins are the same, the crown will move toward who is winning the current match
    if wins1 == wins2:
        if max(hp1,hp2) == 0: displaysurf.blit(HUDAssets[0],(GAMEWIDTH/2-4,MAPHEIGHT+2)) #Display on middle, avoid div by /0
        else:
            crownmove = GAMEWIDTH/2-4-(((hp1-hp2)/max(hp1,hp2))*620)
            displaysurf.blit(HUDAssets[0],(crownmove,MAPHEIGHT+2))
        
        
    
def DrawSuddenDeath(displaysurf,LavaInfo,suddenText,LavaLine):
    '''Receives variables that regulate the lava animation, and the lava to draw and a surface,
    draws and updates lava animation when on sudden death'''
    #Toggle and scroll lava animation on sudden death
    if LavaInfo[0]:
        LavaInfo[1] +=1
    else:
        LavaInfo[1] -=1
    #Lava Goes Up and Down the screen for animation.
    displaysurf.blit(suddenText,(GAMEWIDTH/2-70,MAPHEIGHT+25))
    displaysurf.blit(LavaLine,(0,MAPHEIGHT-32),(LavaInfo[1],0,1280,32))
    if LavaInfo[1] >= 720:LavaInfo[0] = False
    if LavaInfo[1] <= 0: LavaInfo[0] = True
    return LavaInfo
    
