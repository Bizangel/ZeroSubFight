import pygame
from Modules.Sketches import SmallParticles
import Modules.extraFunctions as extra
from random import randint
#import Modules.Sketches as sketches
def pointDistance(x1,y1,x2,y2):
    ''' returns distance between two points'''
    square = (x2-x1)**2 + (y2-y1)**2
    return square**0.5
def midPoint(p1,p2):
    ''' receives two points and returns the midpoint'''
    x1,y1 = p1
    x2,y2 = p2
    return ((x1+x2)/2, (y1+y2)/2)



GAMEWIDTH = 1280
GAMEHEIGHT = 964
MAPHEIGHT = 896
COLD = (159,243,228)
RED = (255,0,0)
LIGHTNING = (209,219,52)
ORANGELIGHTNING = (221,115,12)
class Grenade:
    '''Grenade Class, controls all grenade attributes and characteristics and methods
    for easy track and management of each player grenade'''
    def __init__ (self,x,y,asset,explodeSheet,SFX):
        self.x=x
        self.y=y
        self.SFX = SFX
        self.xvel = 0
        self.yvel = 0
        self.timer = 0
        self.nadetilt = 0
        self.asset = asset
        self.on_ground = False
        self.exploding = False
        self.explodeid = 0
        self.Dmg = 30
        self.explodeSheet = explodeSheet
        self.Bouncy = True
        self.rect = asset.get_rect(centery = y,centerx = x)
    def update(self,blocks,moveBlocks,player,Players,GAMEWIDTH,MAPHEIGHT,suddendeath,xcircular):
        '''Updates the grenade every frame, according to its proper State'''
        player.nadegracetimer +=1
        if not self.on_ground and self.Bouncy:
            self.yvel +=0.1
            if self.yvel > 100: self.yvel = 100
        #Does collision for moving blocks
        fixblockPos = False
        for blockMove in moveBlocks:
            #if pushed by block, be pushed in the block direction
            if blockMove.rect.colliderect(self.rect):
                self.xvel = blockMove.xvel
                
            #if on moving block, add block momentum
            if self.rect.move(0,4).colliderect(blockMove.rect): 
                self.xvel +=blockMove.xvel
                if not self.Bouncy: #update x
                    self.rect.left += blockMove.xvel
                    self.rect.top -= blockMove.yvel
                    #supposed to stop so fix position
                    fixblockPos = True
                break
        #fixes nade on moving blocks
        for blockMove in moveBlocks:
            if blockMove.rect.colliderect(self.rect):
                self.rect.bottom = blockMove.rect.top
        #Does collision and updates according to its velocity
        if self.Bouncy:
            self.rect.left +=self.xvel
            self.collide(self.xvel,0,blocks)
            self.rect.top +=self.yvel
            self.on_ground = False
            self.collide(0,self.yvel,blocks)
            
        #makes y circular only if non suddendeath
        
        if self.rect.top > MAPHEIGHT and not suddendeath: self.rect.bottom = 0
        #Bounce nade off edges if non x circularity
        if not xcircular:
            if self.rect.left < 0:
                self.rect.left = 0
                self.xvel = -self.xvel
            if self.rect.left > GAMEWIDTH:
                self.rect.right = GAMEWIDTH
                self.xvel = -self.xvel
        elif xcircular:
            if self.rect.right <0: self.rect.right = GAMEWIDTH
            if self.rect.left > GAMEWIDTH: self.rect.left = 0
        if player.nade:
            self.timer +=1
        #If nade was triggered
        if player.remotetrigger and player.nadegracetimer > 30:
            self.xvel = 0
            self.yvel = 0
            self.on_ground = True
            player.nade = False
            player.nadeCDStart = True
            self.explode(player,Players)
            self.timer = 0
            player.remotetrigger = False
            self.nadetilt = 0
        #or if nade exploded by time
        if self.timer >= 240:
                self.xvel = 0
                self.yvel = 0
                self.on_ground = True
                player.nade = False
                player.nadeCDStart = True
                self.explode(player,Players)
                self.timer = 0
                self.remotetrigger = False
                self.nadetilt = 0
        #if nade is exploding
        if self.exploding:
            self.explodeid +=1
            if self.explodeid >= 29:
                self.exploding = False
                self.explodeid = 0
                player.nadegracetimer = 0
            


    def collide(self,xvel,yvel,blocks):
        #all blocks that we collide with
        for block in [blocks[i] for i in self.rect.collidelistall(blocks)]:
            if xvel > 0:
                self.rect.right = block.rect.left
                self.xvel = -self.xvel*0.5
                break
                
            elif xvel < 0:
                self.rect.left = block.rect.right
                self.xvel = -self.xvel*0.5
                break
                

            if yvel > 0:
                
                if abs(self.yvel) < 4:
                    self.Bouncy = False
                    
                #Fixes excessive nade tilting
                if abs(self.xvel) > 2: #If has enough "force" to tilt
                    if self.xvel > 0:self.nadetilt -=15
                    elif self.xvel < 0:self.nadetilt +=15
                self.rect.bottom = block.rect.top-6
                self.on_ground = True
                #Apply Friction and bounce
                self.yvel = -self.yvel *0.2
                self.xvel = self.xvel * 0.5
                if not self.Bouncy: self.rect.top +=6

                break
                
                
                
            elif yvel < 0:
                self.rect.top = block.rect.bottom
                self.yvel = -self.yvel * 0.8
                break
    def explode(self,player,Players):
        self.exploding = True
        #Damage Collision Code goes here
        explodeHitbox = pygame.Rect(self.rect.left-55,self.rect.top-69,128,157)
        if Players[0].rect.colliderect(explodeHitbox):
            Players[0].hp -= self.Dmg
            if Players[0].hp < 0: Players[0].hp = 0
            Players[0].hit = True
        if Players[1].rect.colliderect(explodeHitbox):
            Players[1].hp -= self.Dmg
            if Players[1].hp < 0: Players[1].hp = 0
            Players[1].hit = True
        self.SFX.play()
        
        
                
                

class Bullet:
    Bullets1 = []
    Bullets2 = []
    Lightnings1 = [0,[],0] #ball to flash, list of balls, timer
    Lightnings2 = [0,[],0]
    def __init__(self,x,y,xvel,yvel,asset,player,wepID):
        #Assign an ID
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.player = player
        self.asset = asset
        self.wepID = wepID
        lightningappend = False
        if wepID == 0:
            self.Dmg = 3
            self.width,self.height = (self.asset).get_rect().size
            self.rect = pygame.Rect(self.x,self.y,self.width, self.height)

        elif wepID == 1:
            self.Dmg = 15
            self.x2 = x
            self.y2 = y
        elif wepID == 2:
            self.Dmg = 3
            self.rect = pygame.Rect(self.x,self.y,30,30)

            self.animIndex = 0
        elif wepID == 3:
            self.width,self.height = self.asset[4].get_rect().size
            self.width -= 15
            self.height -= 15
            self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
            self.Dmg = 3
            self.animIndex = 0
            self.up = True
            #if abs(self.xvel) > abs(self.yvel): self.angle = 0
            if not player.diagonalDraw and (player.Yfacing == 'U' or player.Yfacing == 'D'):
                #self.ypush = self.yvel
                self.angle = 90
                self.rect.width = self.height
                self.rect.height = self.width
            else:
                self.angle = 0
                #self.ypush = 5
        elif wepID == 4:
            self.width,self.height = self.asset.get_rect().size
            self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
            self.Dmg = 2
            self.flashed = False
            lightningappend = True
            self.flashCounter = 0
            self.timer = 0
            self.despawn = False
            self.pointlist = extra.generatePoints((self.rect.centerx,self.rect.centery),(self.player.rect.centerx,self.player.rect.centery))
            
            
            
        if not lightningappend:
            if player.stringname == 'player1': Bullet.Bullets1.append(self)
            else: Bullet.Bullets2.append(self)
        else:
            if player.stringname == 'player1':
                Bullet.Lightnings1[1].append(self)
                self.color = LIGHTNING
            else:
                Bullet.Lightnings2[1].append(self)
                self.color = ORANGELIGHTNING

    def update(self,player,player1,player2,tileHitbox,moveBlocks):
        if self.wepID == 0:
            self.rect.top -= self.yvel
            self.rect.left += self.xvel
            
            self.collide(player,player1,player2,tileHitbox,moveBlocks)
            
        elif self.wepID == 1:
            self.x2 += self.xvel
            self.y2 -= self.yvel
            if pointDistance(self.x,self.y,self.x2,self.y2) > 100:
                self.x += self.xvel
                self.y -= self.yvel
            self.collide(player,player1,player2,tileHitbox,moveBlocks)
        elif self.wepID == 2:
            self.rect.top -= self.yvel
            self.rect.left += self.xvel
            self.animIndex +=1
            if self.animIndex > 23: self.animIndex = 0
            self.collide(player,player1,player2,tileHitbox,moveBlocks)


        elif self.wepID == 3:
            self.rect.top -= self.yvel
            self.rect.left += self.xvel

            if self.up: self.animIndex +=1
            if self.animIndex > 19: self.up = False
            if not self.up: self.animIndex -= 1
            if self.animIndex == 0: self.up = True
            
            self.collide(player,player1,player2,tileHitbox,moveBlocks)

        elif self.wepID == 4:
            self.rect.top -= self.yvel
            self.rect.left += self.xvel
            #updates flash pointlist
            if self.flashed: self.pointlist = extra.generatePoints((self.rect.centerx,self.rect.centery),(self.player.rect.centerx,self.player.rect.centery))
            #activate randomly
            if self in Bullet.Lightnings1[1]:
                chosen = randint(0,len(Bullet.Lightnings1[1])-1)
                if Bullet.Lightnings1[1][chosen] == self and Bullet.Lightnings1[2] > 15:
                    self.flashed = True
                    
                if Bullet.Lightnings1[1][-1] == self and Bullet.Lightnings1[2] > 15: Bullet.Lightnings1[2] = 0 #if last reset timer
            else:
                chosen = randint(0,len(Bullet.Lightnings2[1])-1)
                if Bullet.Lightnings2[1][chosen] == self and Bullet.Lightnings2[2] > 15:
                    self.flashed = True
                    
                if Bullet.Lightnings2[1][-1] == self and Bullet.Lightnings2[2] > 15: Bullet.Lightnings2[2] = 0 #if last reset timer
                
            if self.despawn:
                self.timer +=1
                if self.timer > 180: self.delete(player1,player2)
            if self.flashed:
                self.flashCounter += 1
                self.flashdamage(player1,player2) #do flashes damage
            self.collide(player,player1,player2,tileHitbox,moveBlocks)
            
            
            
    
    def collide(self,player,player1,player2,tileHitbox,moveBlocks):
        if self.wepID == 0:
            #Plasma Ball
            if self.rect.colliderect(player2.rect) and player == player1:
                if player2.hp != 0:
                    player2.hp -=self.Dmg
                    if player2.hp < 0: player2.hp = 0
                    player2.hit = True
                self.delete(player1,player2)
            elif self.rect.colliderect(player1.rect) and player == player2:
                if player1.hp != 0:
                    player1.hp -=self.Dmg
                    if player1.hp < 0: player1.hp = 0
                    player1.hit = True
                self.delete(player1,player2)
            else:
                if self.rect.collidelist(tileHitbox) !=-1:
                    self.delete(player1,player2)
                #delete if out of bounds
                elif self.rect.centerx < -5 or self.rect.centerx > GAMEWIDTH+5:
                    self.delete(player1,player2)
                #-300 decently above the screen
                elif self.rect.centery < -300 or self.rect.centery > GAMEHEIGHT:
                    self.delete(player1,player2)
                    
        elif self.wepID == 1: #Laser
            #Creates 5 different points on laser, for better collision checking
            pointCheck = []
            pointCheck.append((self.x,self.y))
            midPointRect = midPoint ((self.x,self.y),(self.x2,self.y2))
            pointCheck.append((self.x2,self.y2))
            pointCheck.append(midPointRect)
            pointCheck.append(  midPoint((self.x2,self.y),midPointRect) )
            pointCheck.append(  midPoint((self.x2,self.y2),midPointRect) )
            p1Hit,p2Hit = False,False
            for pCheck in pointCheck:
                if player2.rect.collidepoint(pCheck): p2Hit = True
                if player1.rect.collidepoint(pCheck): p1Hit = True
                
            
            if p2Hit and player == player1:
                if player2.hp != 0:
                    player2.hp -=self.Dmg
                    if player2.hp < 0: player2.hp = 0
                    player2.hit = True
                self.delete(player1,player2)
            elif p1Hit and player == player2:
                if player1.hp != 0:
                    player1.hp -=self.Dmg
                    if player1.hp < 0: player1.hp = 0
                    player1.hit = True
                self.delete(player1,player2)
            else:
                Deleted = False
                for hitbox in tileHitbox:
                    if hitbox.collidepoint(self.x2,self.y2):
                        self.delete(player1,player2)
                        Deleted = True
                        break
                if not Deleted:
                    outOfBounds = True
                    mapBounds = pygame.Rect(0,0,GAMEWIDTH,GAMEHEIGHT)
                    for pCheck in pointCheck:
                        if mapBounds.collidepoint(pCheck):
                            outOfBounds = False
                            break
                    if outOfBounds:
                        self.delete(player1,player2)

                        
        elif self.wepID == 2:
            #boomer
            #Check player collisions and for out of bounds
            if self.rect.colliderect(player2.rect) and player == player1:
                if player2.hp != 0:
                    player2.hp -=self.Dmg
                    if player2.hp < 0: player2.hp = 0
                    player2.hit = True
                    #creates heal particle

                    SmallParticles(player2.rect.centerx,player2.rect.centery,'player1','lifedrain')
                self.delete(player1,player2)
            elif self.rect.colliderect(player1.rect) and player == player2:
                if player1.hp != 0:
                    player1.hp -=self.Dmg
                    if player1.hp < 0: player1.hp = 0
                    player1.hit = True
                    #creates heal particle
                    
                    SmallParticles(player1.rect.centerx,player1.rect.centery,'player2','lifedrain')
                self.delete(player1,player2)
            #delete if out of bounds
            elif self.rect.centerx < -5 or self.rect.centerx > GAMEWIDTH+5:
                self.delete(player1,player2)
            #-300 decently above the screen
            elif self.rect.centery < -300 or self.rect.centery > GAMEHEIGHT:
                self.delete(player1,player2)


                
        elif self.wepID == 3:
            #soundwave
            if self.rect.colliderect(player2.rect) and player == player1:
                if player2.hp != 0:
                    player2.hp -=self.Dmg
                    if player2.hp < 0: player2.hp = 0
                    player2.hit = True
                    player2.pushhit = True
                    player2.momentum[0] = self.xvel *(1/2)
                    player2.momentum[1] = self.yvel * (1/4)
                    

                    
                self.delete(player1,player2)

            elif self.rect.colliderect(player1.rect) and player == player2:
                if player1.hp != 0:
                    player1.hp -=self.Dmg
                    if player1.hp < 0: player1.hp = 0
                    player1.hit = True
                    player1.pushhit = True
                    player1.momentum[0] = self.xvel *(1/2)
                    player1.momentum[1] = self.yvel * (1/4)
                    
                self.delete(player1,player2)
            else:
                if self.rect.collidelist(tileHitbox) !=-1:
                    self.delete(player1,player2)
                    
                elif self.rect.centerx < -5 or self.rect.centerx > GAMEWIDTH+5:
                    self.delete(player1,player2)
                #-300 decently above the screen
                elif self.rect.centery < -300 or self.rect.centery > GAMEHEIGHT:
                    self.delete(player1,player2)

        elif self.wepID == 4:
            if self.rect.colliderect(player2.rect) and player == player1:
                if player2.hp != 0 and not player2.hit:
                    player2.hp -=self.Dmg
                    if player2.hp < 0: player2.hp = 0
                    player2.hit = True
                    
            elif self.rect.colliderect(player1.rect) and player == player2:
                if player1.hp != 0 and not player1.hit:
                    player1.hp -=self.Dmg
                    if player1.hp < 0: player1.hp = 0
                    player1.hit = True
            else:
                #stop if hits something
                for moveBlock in moveBlocks:
                    if self.rect.colliderect(moveBlock.rect):
                        #attach to it
                        self.xvel,self.yvel = 0,0 #stop and attach
                        self.rect.left += moveBlock.xvel
                        self.rect.top -= moveBlock.yvel
                        self.despawn = True
                        return #it's attached. and so it will be.
                    
                if self.rect.collidelist(tileHitbox) !=-1:
                    self.xvel,self.yvel = 0,0
                    self.despawn = True
                elif self.rect.centerx < -5 or self.rect.centerx > GAMEWIDTH+5:
                    self.delete(player1,player2)
                elif self.rect.centery < -300 or self.rect.centery > GAMEHEIGHT:
                    self.delete(player1,player2)

            
            
                        
    def flashdamage(self,player1,player2):
        p1 = (self.rect.centerx,self.rect.centery)
        p2 = (self.player.rect.centerx,self.player.rect.centery)
        if self.player.stringname == 'player1':
            if extra.rectlinecollide(player2.rect,p1,p2):
                if not player2.flashhit:
                    player2.hp -= 10
                    if player2.hp < 0: player2.hp = 0
                    player2.flashhit = True
                    player2.hit = True
        else:
            if extra.rectlinecollide(player1.rect,p1,p2):
                if not player1.flashhit:
                    player1.hp -= 10
                    if player1.hp < 0: player1.hp = 0
                    player1.flashhit = True
                    player1.hit = True
            
            
        
                
    def flash(self,surface):
        
        pygame.draw.lines(surface,self.color,False,self.pointlist,10)
        if self.flashCounter > 8:
            #Do collideHit Calculation by lightnings
            self.flashCounter = 0
            self.flashed = False
                
    def draw(self,surface):
        if self.wepID == 0:surface.blit(self.asset,(self.rect))
        elif self.wepID == 1: pygame.draw.line(surface,(255,0,0),(self.x,self.y),(self.x2,self.y2),5)
        elif self.wepID == 2: surface.blit(self.asset,self.rect,( (self.animIndex//3)*30,0,30,30))
        elif self.wepID == 3:
            img = pygame.transform.rotate(self.asset[self.animIndex//4],self.angle)
            surface.blit(img,self.rect)
            
        elif self.wepID == 4: 
                    
            if self.flashed: self.flash(surface)
            
            surface.blit(self.asset,(self.rect))
            
            
            
                    
            

            

            

    def delete(self,player1,player2):
        #Delete Player 1 Bullets
        if self.wepID != 4:
            if self.player == player1:
                deleter = Bullet.Bullets1.index(self)
                del Bullet.Bullets1[deleter]
            elif self.player == player2:
                deleter = Bullet.Bullets2.index(self)
                del Bullet.Bullets2[deleter]
        else:
            if self.player.stringname == 'player1':
                deleter = Bullet.Lightnings1[1].index(self)
                del Bullet.Lightnings1[1][deleter]
            else:
                deleter = Bullet.Lightnings2[1].index(self)
                del Bullet.Lightnings2[1][deleter]
            

class WeaponChip:
    chips = []
    def __init__(self,pos,asset,wepID):
        self.asset = asset
        self.rect = pygame.Rect((pos[0],pos[1]),asset.get_size())
        self.wepID = wepID
        self.active = True
        self.timer = 0
        WeaponChip.chips.append(self)
    def update(self):
        self.timer +=1
    def draw(self,displaysurf):
        if self.timer > 360: #6 seconds start flashing
            if 360 <= self.timer <= 420 and self.timer%8 != 1: displaysurf.blit(self.asset,self.rect) #flashes every 8frames
            elif 420 <= self.timer <= 450 and self.timer%4 != 1: displaysurf.blit(self.asset,self.rect) #flashes every 4frames
            elif 450 <= self.timer <= 480 and self.timer%2 != 1: displaysurf.blit(self.asset,self.rect) #flashes every 2frames
            elif self.timer > 480:
                self.delete() #Delete after 8s
        else: displaysurf.blit(self.asset,self.rect)
        
        
    def delete(self):
        deleter = WeaponChip.chips.index(self)
        del WeaponChip.chips[deleter]
    def activate(self,player):
        player.setWeapon(self.wepID)
        self.delete()
    
    
        
