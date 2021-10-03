import pygame
from math import cos,sin,radians
from weaponry import *
from collections import namedtuple
from Modules.wepFixes import wepAdjust
import Modules.extraFunctions as extra

MAPHEIGHT =896
GAMEWIDTH=1280
GAMEHEIGHT=964
    
spritetoID = {
    'idleleft':0,
    'idleright':1,
    'idlerightup':2,
    'idlerightdown':3,
    'idleleftup':4,
    'idleleftdown':5,
    'jumpleft':6,
    'jumpright':7,
    'jumpleftup': 8,
    'jumprightup':9,
    'jumpleftdown':10,
    'jumprightdown':11,
    'jumpdownL':12,
    'jumpdownR':13,
    'jumpupL':14,
    'jumpupR':15,
    'runL':16,
    'runLU':17,
    'runLD':18,
    'runR':19,
    'runRU':20,
    'runRD':21,
    'stillleftdown': 22,
    'stillleftup': 23,
    'stillrightdown': 24,
    'stillrightup': 25,
    'deathredleft':26,
    'deathredright':27,
    'hitleft':28,
    'hitright':29,
    'deathexplosion': 30,
    'finaldeathexplosion': 31
    }
Move = namedtuple('move',['up','left','right'])
class Player:
    Players = []
    def __init__ (self,spawnPos,xface,spriteList,grenade,stringname,SFXList):
        #Name as string, for various things
        self.stringname = stringname
        #assets
        self.spriteList = spriteList
        self.Xfacing = xface
        self.Yfacing = 0
        self.animIndex = -1
        self.animDisplay = 0
        self.x,self.y= spawnPos
        self.xvel = 0
        self.yvel = 0
        self.drawground = False #Determines if player to be drawn as in Air or not.
        #Game Mechanics
        self.alive = True
        self.on_ground = False
        self.move_speed = 5
        self.jump_speed = 12
        self.hp = 300
        self.hit = False
        self.pushhit = False

        self.momentum = [0,0] #reduced greatly on collision and every frame, only applied by wep
        
        self.hitcounter = 0
        self.pushhitcounter = 0
        self.currentWeapon = 0 #Current weapon ID, check weaponry dictionary for names
        #Move, will change to NamedTuple Move(Up,left,right)
        self.move = Move(False,False,False)
        #Nade Mechanics, Fire Mechanics
        self.bulx,self.buly = 0,0 #where bullets come out from
        self.optBulxvel,self.optBulyvel = 0,0 #If player mouse too close or stick is deadzone, shoot based on facing
        self.overheat = False
        self.overheatCounter = 0
        self.didShoot = False
        self.nadegracetimer = 0
        self.win = True
        self.nadeCDTimer = 0
        self.nadeCDStart = False
        self.remotetrigger= False
        self.shootCD = False
        self.shootCDTimer = 0
        self.nadeCD = True
        self.nade = False
        self.nadeForce = 7  #Nade speed
        self.grenade = grenade
        self.shootRadAngle = 0
        self.Wins = 0 #win tracker

        #regulates how often flashhit damage is dealt
        self.flashhit = False
        self.flashhitcounter = 0
        
        self.teleportSFX,self.explodeSFX = SFXList
        
        self.mouseTrack = False
        self.diagonalDraw = False
        self.state = None
        self.weaponTimer = 0 #Determines how much time left in weapon hand

        self.bulletSpeed = 30
        self.shootFrameTrueCD = 5
        #Id for explosions animations
        self.explodeIDTimer = 0
        self.explodeID = 0
        self.explodeSeconds = 0
        self.finalexplodeID = -1
        self.exploding = True

        self.angle = None
        self.shootAngle = 0
        self.no360 = False

        self.pause = False
        self.pauseCounter = 0
        self.recentlyPaused = False
        #Player Rect 
        self.width,self.height = (self.spriteList[0]).get_rect().size
        self.width = 28
        self.rect = pygame.Rect(self.x,self.y,self.width, self.height)
    def update(self,move,blocks,moveBlocks,Tilemap,tileHitbox,Players,suddendeath,Circularity,gameMap,cursorRect):
        GAMEWIDTH = 1280
        MAPHEIGHT = 896
        xcircular = Circularity[0]
        ycircular = Circularity[1]
        if not self.pushhit:
            if move.up and self.on_ground  and self.hp > 0:  
                self.yvel -= self.jump_speed
            if move.left:
                self.xvel = -self.move_speed
                if self.angle == None: self.Xfacing = 'L' #if no angle override
            if move.right:
                self.xvel = self.move_speed
                if self.angle == None: self.Xfacing = 'R'

            if not(move.left or move.right):
                self.xvel= 0
                self.animIndex = -1

            if not self.on_ground: #apply gravity and remove y momentum
                self.removeMomentum(True)
                self.yvel +=0.3
                if self.yvel > 100: self.yvel = 100
            
        
        
        #Update direction according to mouse/rightstick
        if self.mouseTrack:
            currPos = [self.rect.centerx,self.rect.centery]
            currPos[1] = GAMEHEIGHT - currPos[1]
            mousePosx,mousePosy = cursorRect.centerx,cursorRect.centery
            mousePosy = GAMEHEIGHT-mousePosy
            self.setAngle( extra.pointToAngle(currPos,(mousePosx,mousePosy)) )
            if self.angle == None:
                self.state = None
                self.shootAngle = None
            else:
                self.state = extra.angletoState(self.angle)
            self.stateUpdate()
            self.optBulxvel,self.optBulyvel = self.weaponAdjust()
            if self.angle != None:
                self.shootAngle = extra.pointToAngle((self.bulx,GAMEHEIGHT-self.buly),(mousePosx,mousePosy),False) #Will always give an angle
                if self.move.left or self.move.right:
                    #Cap Up
                    if 45 <= self.shootAngle <= 90: self.shootAngle = 45
                    elif 90 <= self.shootAngle <= 135: self.shootAngle = 135
                    #Cap Down
                    if 225 <= self.shootAngle <= 270: self.shootAngle = 225
                    elif 270 <= self.shootAngle <= 315: self.shootAngle = 315
        else:
            if self.no360: #If no mousetracking and no controller
                self.optBulxvel,self.optBulyvel = self.weaponAdjust()
                self.state = None
                self.shootAngle = None
        
        #If not mousetrack, shootangle calculation is done on gameControls
        
        #allow jump on suddendeath lava
        if suddendeath and self.rect.bottom > MAPHEIGHT-15 and self.hp > 0:
            if move.up: self.yvel -=self.jump_speed
        
  
        #sets boundaries only if non X circular
        if not xcircular:
            if self.rect.left < 0:
                self.rect.left = 0
                self.removeMomentum()
            if self.rect.right > GAMEWIDTH:
                self.rect.right = GAMEWIDTH
                self.removeMomentum()
        #if X circularity enabled
        elif xcircular:
            if self.rect.right < 0: self.rect.right = GAMEWIDTH
            if self.rect.left > GAMEWIDTH: self.rect.left = 0
        #makes y circular
        if not suddendeath and ycircular:
            if self.rect.top > MAPHEIGHT: self.rect.bottom = 0
        #If noncircular allows for jump, and returns back
        elif suddendeath:
            #Does Lava Damage -------------------------------------------- LAVA DAMAGE
            if self.rect.bottom >= MAPHEIGHT-32 and self.hp >0:
                self.hp -=5
                if self.hp < 0: self.hp = 0
            #Removes Y circularity on sudden death
            if self.rect.bottom >= MAPHEIGHT:
                self.rect.bottom = MAPHEIGHT-5
                self.yvel = 0
                self.on_ground = True
        #Map 3 lightning damage --------------------- LIGHTNING DAMAGE
        if gameMap == 3 and self.rect.top < 10:
            self.hp -=3
            if self.hp < 0: self.hp = 0
        #Checks moving blocks updates
        for blockMove in moveBlocks:
            #if pushed by block, be pushed in the block direction
            
            if blockMove.rect.colliderect(self.rect):
                self.xvel = blockMove.xvel

            #if on moving block, add block momentum and fix feet beforehand
            if self.rect.move(0,4).colliderect(blockMove.rect):
                self.on_ground = True
                self.xvel +=blockMove.xvel
                if self.drawground:self.rect.bottom = blockMove.rect.top

                #remove momentum
                self.removeMomentum()
                
                #self.drawground = True
                break
            
        if abs(self.momentum[0]) < 1.5: self.momentum[0] = 0
        if abs(self.momentum[1]) < 1.5: self.momentum[1] = 0
        
        self.xvel += self.momentum[0] #adds momentum to speed
        self.yvel -= self.momentum[1]
        #update pos
        self.rect.left +=self.xvel
        self.collide(self.xvel,0,   blocks,gameMap,GAMEWIDTH)

        #Checks for Y in moveBlocks
        for blockMove in moveBlocks:
            if self.rect.move(0,4).colliderect(blockMove.rect):
                if not self.move.up:
                    self.yvel =-blockMove.yvel
                    if blockMove.yvel != 0: self.rect.bottom = blockMove.rect.top
                else:
                    self.rect.bottom = blockMove.rect.top -2
                    self.yvel = -self.jump_speed
                #remove momentum
                self.removeMomentum()

            
        self.rect.top +=self.yvel
        self.on_ground = False
        self.collide(0,self.yvel,   blocks,gameMap,GAMEWIDTH)            

        if not self.shootCD:
            self.shootCDTimer +=1
        if self.shootCDTimer >= self.shootFrameTrueCD:    #How fast can player shoot ---------
            self.shootCDTimer = 0
            self.shootCD = True
        #Nade updates
        if self.nade or self.grenade.exploding:
            self.grenade.update(Tilemap,moveBlocks,self,Players,GAMEWIDTH,MAPHEIGHT,suddendeath,xcircular)
        #Nades CD
        if self.nadeCDStart:
            self.nadeCDTimer +=1
            if self.nadeCDTimer >= 600:
                self.nadeCD = True
                self.nadeCDStart = False
                self.nadeCDTimer = 0
        
        #Update animation Index 
        self.animIndex +=1
        if self.animIndex > 55: self.animIndex = 0
        self.animDisplay = self.animIndex // 8

        #Updates if on ground or not for ground animations
        self.drawground = False
        if self.rect.move(0,4).collidelist(tileHitbox) != -1: self.drawground = True #If block is at least 4 pixels below
        #updates hit animation
        if self.hit:
            if self.hitcounter == 3:       #How much frames hit visual lasts
                self.hit = False
                self.hitcounter = 0
            else:
                self.hitcounter +=1
        if self.pushhit: self.pushhit = False

        if self.flashhit:
            self.flashhitcounter +=1
            if self.flashhitcounter >9:
                self.flashhit = False
                self.flashhitcounter = 0

        
        #Updates weapon timer ---------
        if self.currentWeapon != 0:
            self.weaponTimer +=1
            if self.currentWeapon == 1 and self.weaponTimer > 720: self.setWeapon(0)
            elif self.currentWeapon == 2 and self.weaponTimer > 720: self.setWeapon(0)
            elif self.currentWeapon == 3 and self.weaponTimer > 720: self.setWeapon(0)
            elif self.currentWeapon == 4 and self.weaponTimer > 720: self.setWeapon(0)
                
                

        
        #Overheat ----------------------
        #Set overheat according to wep
        if self.currentWeapon == 0: wepOverheat = (30,3,7)
        elif self.currentWeapon== 1: wepOverheat = (150,3,20)
        elif self.currentWeapon== 2: wepOverheat = (40,5,10)
        elif self.currentWeapon== 3: wepOverheat = (50,3,10)
        elif self.currentWeapon== 4: wepOverheat = (1001,0,15)


        '''Overheat Mechanic'''
        
        if self.didShoot and not self.overheat: self.overheatCounter += wepOverheat[0] #if shoot increases
        if not self.didShoot and not self.overheat: self.overheatCounter -= wepOverheat[1] #If not shooting reduce overheat while can still shoot
        if self.overheat: self.overheatCounter -= wepOverheat[2] #Reduce overheat counter when can't shoot
        if self.overheatCounter > 1000:
            self.overheat = True
            self.overheatCounter = 1000
        
        if self.overheatCounter < 0: self.overheatCounter,self.overheat = 0,False #caps it at 0 and disables
    def trypause(self,canPause): #attempts to pause
        if canPause and not self.recentlyPaused:
            if self.pause: self.pause = False
            else: self.pause = True
            self.recentlyPaused = True
    def removeMomentum(self,vertical=None):
        if vertical == None:
            if self.momentum[0] > 0: self.momentum[0] -= 1
            elif self.momentum[0] < 0: self.momentum[0] += 1
            
            if self.momentum[1] > 0: self.momentum[1] -= 1
            elif self.momentum[1] < 0: self.momentum[1] += 1
        elif vertical == True:
            if self.momentum[1] > 0: self.momentum[1] -= 1
            elif self.momentum[1] < 0: self.momentum[1] += 1

    def collide(self,xvel,yvel,blocks,gameMap,GAMEWIDTH):
        #all blocks that we collide with
        for block in [blocks[i] for i in self.rect.collidelistall(blocks)]:
            #remove momentum cuz collided
            self.removeMomentum()
            
            if xvel > 0:
                self.rect.right = block.rect.left
                return
                
            if xvel < 0:
                self.rect.left = block.rect.right
                return

            if yvel > 0:
                self.rect.bottom = block.rect.top
                self.on_ground = True
                self.yvel = 0
                #If Map and is hotblock 
                if gameMap == 2 and block.assetStringname == 'mtsHotBlock':
                    self.on_ground = False
                    self.yvel = -17
                #If map and teleporter
                if gameMap == 2 and block.assetStringname == 'mtsTeleporter':
                    self.teleportSFX.play()
                    if self.rect.left < GAMEWIDTH/2:
                        #left teleporter
                        self.rect.bottom = 192
                        self.rect.right = GAMEWIDTH-15
                        return 
                    else:
                        #right teleporter
                        self.rect.bottom = 192
                        self.rect.left = 15
                        return
                        
            
            if yvel < 0:
                self.rect.top = block.rect.bottom
                self.yvel = 0
                return
        
    def Shoot(self,bulletasset):
        '''Triggers the shoot command, attempts to shoot if the player can shoot, and creates Bullet object according to player position and facing'''
        
        #Sets bullet speed according to weapon type
        if self.currentWeapon == 0: Bvel = self.bulletSpeed 
        elif self.currentWeapon == 1: Bvel = self.bulletSpeed * (5/3)
        elif self.currentWeapon == 2: Bvel = self.bulletSpeed * (1/2)
        elif self.currentWeapon == 3: Bvel = self.bulletSpeed * (1/2)
        elif self.currentWeapon == 4: Bvel = self.bulletSpeed * (1/10)
        
        if self.shootCD and self.hp > 0 and not self.overheat: #Only if can shoot, not read every frame
            self.didShoot = True
            if self.state == None: bulletxvel,bulletyvel,self.shootAngle = self.optBulxvel,self.optBulyvel,self.optAngle
            else:
                bulletxvel = cos(radians(self.shootAngle))*Bvel
                bulletyvel = sin(radians(self.shootAngle))*Bvel
                
            if self.currentWeapon == 4: #Create volley
                self.shootAngle += 45
                for i in range(7):
                    bulletxvel = cos(radians(self.shootAngle))*Bvel
                    bulletyvel = sin(radians(self.shootAngle))*Bvel
                    Bullet(self.bulx,self.buly,bulletxvel,bulletyvel,bulletasset,self,self.currentWeapon)
                    self.shootAngle -=18
                    
            else:
                Bullet(self.bulx,self.buly,bulletxvel,bulletyvel,bulletasset,self,self.currentWeapon)
                
            self.shootCD = False
            
            
    def weaponAdjust(self):
        if self.currentWeapon == 0: Bvel = self.bulletSpeed
        elif self.currentWeapon == 1: Bvel = self.bulletSpeed*(5/3)
        elif self.currentWeapon == 2: Bvel = self.bulletSpeed *(1/2)
        elif self.currentWeapon == 3: Bvel = self.bulletSpeed *(1/2)
        elif self.currentWeapon == 4: Bvel = self.bulletSpeed * (1/10)
        
        if self.drawground:
            if not self.move.right and not self.move.left:
                if self.Yfacing == 0:
                    if self.Xfacing == 'R': bulletxvel,bulletyvel,bulx,buly,a = Bvel,0, self.rect.right,self.rect.top+10, 0
                    elif self.Xfacing =='L': bulletxvel,bulletyvel,bulx,buly,a  = -Bvel,0 , self.rect.left,self.rect.top+10, 180

                elif self.Yfacing == 'U':
                    if self.Xfacing == 'R': bulletxvel,bulletyvel,bulx,buly,a   = 0,Bvel , self.rect.left+13,self.rect.top, 90
                    elif self.Xfacing =='L':bulletxvel,bulletyvel,bulx,buly,a   = 0,Bvel , self.rect.right-28,self.rect.top, 90
                
                elif self.Yfacing == 'D':
                    if self.Xfacing == 'R': bulletxvel,bulletyvel,bulx,buly,a = 0,-Bvel , self.rect.right-25 , self.rect.bottom, 270
                    elif self.Xfacing == 'L':bulletxvel,bulletyvel,bulx,buly,a = 0,-Bvel , self.rect.left+10,self.rect.bottom, 270
        
            elif self.Xfacing == 'R':
                if self.Yfacing == 0: bulletxvel,bulletyvel,bulx,buly,a = Bvel,0, self.rect.right,self.rect.top+10, 0
                elif self.Yfacing == 'U': bulletxvel,bulletyvel,bulx,buly,a  = Bvel,Bvel  ,self.rect.right-15,self.rect.top, 45
                elif self.Yfacing == 'D':bulletxvel,bulletyvel,bulx,buly,a  = Bvel,-Bvel  ,self.rect.right-15,self.rect.bottom , 315
            elif self.Xfacing == 'L':
                if self.Yfacing == 0: bulletxvel,bulletyvel,bulx,buly,a  = -Bvel,0 , self.rect.left,self.rect.top+10 , 180
                elif self.Yfacing == 'U': bulletxvel,bulletyvel,bulx,buly,a  = -Bvel,Bvel  ,self.rect.left+10,self.rect.top , 135
                elif self.Yfacing == 'D': bulletxvel,bulletyvel,bulx,buly,a  = -Bvel,-Bvel ,self.rect.left+10,self.rect.bottom , 225
        else:
            if not self.move.right and not self.move.left:
                    if self.Yfacing == 0:
                        if self.Xfacing == 'R': bulletxvel,bulletyvel,bulx,buly,a  = Bvel,0 ,self.rect.right,self.rect.top+10, 0
                        elif self.Xfacing == 'L': bulletxvel,bulletyvel,bulx,buly,a  = -Bvel,0 ,self.rect.left,self.rect.top+10, 180
                    elif self.Yfacing == 'U': bulletxvel,bulletyvel,bulx,buly,a  = 0,Bvel ,self.rect.right-15,self.rect.top, 90
                    elif self.Yfacing == 'D': bulletxvel,bulletyvel,bulx,buly,a  = 0,-Bvel ,self.rect.right-15,self.rect.bottom , 270
            else:
                if self.Xfacing == 'R':
                    if self.Yfacing == 0: bulletxvel,bulletyvel,bulx,buly,a  = Bvel,0 ,self.rect.right,self.rect.top+10, 0
                    elif self.Yfacing == 'U': bulletxvel,bulletyvel,bulx,buly,a  = Bvel,Bvel ,self.rect.right-15,self.rect.top, 45
                    elif self.Yfacing == 'D': bulletxvel,bulletyvel,bulx,buly,a  = Bvel,-Bvel ,self.rect.right-15,self.rect.bottom, 315

                elif self.Xfacing == 'L':
                    if self.Yfacing == 0: bulletxvel,bulletyvel,bulx,buly,a  = -Bvel,0 ,self.rect.left,self.rect.top+10, 180
                    elif self.Yfacing == 'U': bulletxvel,bulletyvel,bulx,buly,a = -Bvel,Bvel ,self.rect.left+10,self.rect.top, 135
                    elif self.Yfacing == 'D': bulletxvel,bulletyvel,bulx,buly,a = -Bvel,-Bvel ,self.rect.left+10,self.rect.bottom, 225


        self.bulx,self.buly = wepAdjust(self.currentWeapon,bulx,buly,self.Xfacing,self.Yfacing,self.drawground,(not self.move.right and not self.move.left),self.diagonalDraw )
        optionalBulletxvel, optionalBulletyvel = bulletxvel,bulletyvel
        self.optAngle = a
        return (optionalBulletxvel,optionalBulletyvel)
    def stateUpdate(self):
        '''Updates the players facing according to the attribute state of the player'''
        if self.state == None: self.diagonalDraw = False #Deadzoned or on player rect
        else:
            if len(self.state) == 3:
                self.Xfacing,self.Yfacing,self.diagonalDraw = self.state
            else:
                self.diagonalDraw = True
                self.Xfacing,self.Yfacing = self.state

    def setAngle(self,angle):
        '''Receives an angle and if player is moving and angle is too above/low caps it, and then sets it'''
        if angle != None:
            if self.move.left or self.move.right:
                #Cap Up
                if 45 <= angle <= 90: angle = 45
                elif 90 <= angle <= 135: angle = 135
                #Cap Down
                if 225 <= angle <= 270: angle = 225
                elif 270 <= angle <= 315: angle = 315
                    
        self.angle = angle
                
    def nadethrow(self):
        if self.nade: #If nade is active
            self.remotetrigger = True
        elif self.nadeCD and self.hp > 0:
            #Throws nade
            self.nade = True 
            self.nadeCD = False
            self.grenade.rect.top = self.rect.top
            self.grenade.rect.left = self.rect.left
            self.grenade.Bouncy = True #Ensures initial bouncyness
            if self.shootAngle == None:
                if not self.diagonalDraw and self.Yfacing == 'U':
                    self.shootAngle = 90
                elif not self.diagonalDraw and self.Yfacing == 'D':
                    self.shootAngle = 270
                elif self.Xfacing == 'R': self.shootAngle = 30
                elif self.Xfacing == 'L': self.shootAngle = 150
            self.grenade.xvel = cos(radians(self.shootAngle))*self.nadeForce
            self.grenade.yvel= -sin(radians(self.shootAngle))*self.nadeForce
    def deathanimation(self,surface):
        deathexplosion = self.spriteList[spritetoID['deathexplosion']]
        finaldeathexplosion = self.spriteList[spritetoID['finaldeathexplosion']]
        self.explodeIDTimer +=1
        self.explodeID +=1
        self.explodeSeconds +=1
        
        if self.explodeSeconds < 180:
            if self.explodeID//7 == 0:surface.blit(deathexplosion,(self.rect.left,self.rect.top+5),((self.explodeID//7)*32,0,32,32))
            elif self.explodeID//7 == 1:surface.blit(deathexplosion,(self.rect.left,self.rect.top+20),((self.explodeID//7)*32,0,32,32))
            elif self.explodeID//7 == 2:surface.blit(deathexplosion,(self.rect.left+8,self.rect.top+26),((self.explodeID//7)*32,0,32,32))
            elif self.explodeID//7 == 3:surface.blit(deathexplosion,(self.rect.right-32,self.rect.top+15),((self.explodeID//7)*32,0,32,32))
            elif self.explodeID//7 == 4:surface.blit(deathexplosion,(self.rect.right-32,self.rect.top+5),((self.explodeID//7)*32,0,32,32))
            elif self.explodeID//7 == 5:surface.blit(deathexplosion,(self.rect.left+12,self.rect.top),((self.explodeID//7)*32,0,32,32))
            if self.explodeIDTimer > 55: self.explodeIDTimer = 0
            if self.explodeID > 55: self.explodeID = 0
        #Remove speed
        if self.explodeSeconds == 180: self.explodeSFX.play()
        if self.explodeSeconds == 1: self.move_speed = 0
        if self.explodeSeconds > 180:
            self.finalexplodeID +=1
            surface.blit(finaldeathexplosion,(self.rect.left-38,self.rect.top-65),((self.finalexplodeID//4)*128,0,128,128))
            if self.finalexplodeID > 10:
                self.alive = False
            if self.finalexplodeID > 47:
                self.exploding = False
                self.win = False
            
    def setWeapon(self,weapon):
        '''Receives a weapon and sets it as the user gun'''
        self.weaponTimer = 0
        self.currentWeapon = weapon
        if weapon == 0: self.shootFrameTrueCD = 5
        elif weapon == 1: self.shootFrameTrueCD = 15
        elif weapon == 2: self.shootFrameTrueCD = 7
        elif weapon == 3: self.shootFrameTrueCD = 7
    def Reset(self,spawnPos,facing):
        '''Receives where to spawn the player, and where to face, and resets the player ready for a new map'''
        #Name as string, for various things
        self.Xfacing = facing
        self.Yfacing = 0
        self.rect.left,self.rect.top = spawnPos

        self.animIndex = -1
        self.animDisplay = 0
        self.xvel = 0
        self.yvel = 0
        #Reset to normal Values
        self.alive = True
        self.on_ground = False
        self.move_speed = 5
        self.jump_speed = 12
        self.nadeForce = 7
        
        self.hp = 300
        self.hit = False
        self.hitcounter = 0
        self.currentWeapon = 0
        self.weaponTimer = 0
        
        self.overheat = False
        self.overheatCounter = 0
        self.didShoot = False
        self.nadegracetimer = 0
        self.win = True
        self.nadeCDTimer = 0
        self.nadeCDStart = False
        self.remotetrigger= False
        self.shootCD = False
        self.shootCDTimer = 0
        self.nadeCD = True
        self.nade = False

        self.bulletSpeed = 30
        self.shootFrameTrueCD = 5
        #Id for explosions animations
        self.explodeIDTimer = 0
        self.explodeID = 0
        self.explodeSeconds = 0
        self.finalexplodeID = -1
        self.exploding = True
    def drawNade(self,displaysurf):
        '''Receives a display surface and draws the player's nade properly'''
        if self.nade:
            displaysurf.blit(pygame.transform.rotate(self.grenade.asset,self.grenade.nadetilt),self.grenade.rect)
        elif self.grenade.exploding:
            displaysurf.blit(self.grenade.explodeSheet,(self.grenade.rect.left-55,self.grenade.rect.top-69),((self.grenade.explodeid//3*128),0,128,157))
        
    def Draw(self,displaysurf):
        '''Receives a displaysurf and draws player and grenade accordingly to its state in the surface'''
        #Draws Player
        playerStill = not self.move.right and not self.move.left
        #if self.topdownOverride: playerStill = True
        
        if self.hp == 0 and self.exploding:
            self.deathanimation(displaysurf)#Dying
        
        if self.hit and self.alive: #If player was hit and is alive
            if self.Xfacing == 'R': state = 'hitright'
            elif self.Xfacing == 'L': state = 'hitleft'
        elif self.alive and self.hp == 0: #If dying
            if self.Xfacing == 'L': state = 'deathredleft'
            elif self.Xfacing == 'R': state = 'deathredright'
    
        elif self.drawground:
            if playerStill:
                #Draw straight left/right
                if self.Xfacing == 'L' and self.Yfacing == 0: state = 'idleleft'
                elif self.Xfacing == 'R' and self.Yfacing == 0: state = 'idleright'
                
                elif self.diagonalDraw:
                    if self.Xfacing == 'L' and self.Yfacing == 'U': state = 'stillleftup'
                    elif self.Xfacing == 'L' and self.Yfacing == 'D': state = 'stillleftdown'
                    elif self.Xfacing == 'R' and self.Yfacing == 'U': state = 'stillrightup'
                    elif self.Xfacing == 'R' and self.Yfacing == 'D': state = 'stillrightdown'
                else:
                    if self.Xfacing == 'L' and self.Yfacing == 'U': state = 'idleleftup'
                    elif self.Xfacing == 'L' and self.Yfacing == 'D': state = 'idleleftdown'
                    elif self.Xfacing == 'R' and self.Yfacing == 'U': state = 'idlerightup'
                    elif self.Xfacing == 'R' and self.Yfacing == 'D': state = 'idlerightdown'
            if self.move.right or self.move.left:
                if self.Xfacing == 'R':
                    if self.Yfacing == 0: state = 'runR'
                    elif self.Yfacing == 'U': state= 'runRU'
                    elif self.Yfacing =='D': state = 'runRD'
                elif self.Xfacing == 'L':
                    if self.Yfacing == 0: state = 'runL'
                    elif self.Yfacing == 'U': state = 'runLU'
                    elif self.Yfacing =='D': state = 'runLD'
        else:
            if playerStill:
                if self.Xfacing == 'L' and self.Yfacing == 0: state ='jumpleft'
                elif self.Xfacing == 'R' and self.Yfacing == 0: state= 'jumpright'
                elif self.diagonalDraw:
                    if self.Xfacing == 'L' and self.Yfacing == 'U': state = 'jumpleftup'
                    elif self.Xfacing == 'L' and self.Yfacing == 'D': state = 'jumpleftdown'
                    elif self.Xfacing == 'R' and self.Yfacing == 'U': state = 'jumprightup'
                    elif self.Xfacing == 'R' and self.Yfacing == 'D': state = 'jumprightdown'
                else:
                    if self.Yfacing == 'U':
                        if self.Xfacing == 'L': state = 'jumpupL'
                        elif self.Xfacing == 'R': state = 'jumpupR'
                    elif self.Yfacing == 'D':
                        if self.Xfacing == 'L': state ='jumpdownL'
                        elif self.Xfacing == 'R': state ='jumpdownR'
            else:
                
                if self.Xfacing == 'L':
                    if self.Yfacing == 0: state ='jumpleft'
                    elif self.Yfacing == 'U': state ='jumpleftup'
                    elif self.Yfacing == 'D': state ='jumpleftdown'
                elif self.Xfacing == 'R':
                    
                    if self.Yfacing == 0: state = 'jumpright'
                    elif self.Yfacing == 'U':state = 'jumprightup'
                    elif self.Yfacing == 'D': state = 'jumprightdown'
        
        if state != None :sprite = self.spriteList[spritetoID[state]]
        if (self.move.right or self.move.left) and self.drawground and self.hp!= 0 and not self.hit: #Running animations spritesheet cut needed.
            if self.Yfacing == 'U': displaysurf.blit(sprite,(self.rect),(self.animDisplay*50,0,50,52))
            else: displaysurf.blit(sprite,(self.rect),(self.animDisplay*50,0,50,50))
        elif (state == 'stillleftdown' or state == 'stillrightdown') and self.hp != 0: displaysurf.blit(sprite,(self.rect).move(0,-7))
        elif playerStill and self.Yfacing == 'U' and self.drawground and self.hp != 0: displaysurf.blit(sprite,(self.rect).move(0,-7))
        else:
            #Most cases
            if self.alive: displaysurf.blit(sprite,(self.rect))
        
        
