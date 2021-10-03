import pygame
from Modules.assets import *
MAPHEIGHT =896
GAMEWIDTH=1280
GAMEHEIGHT=964
LIGHTNING = (209,219,52)
def getGroup(getstring):
    '''Receives a returns the grouplist of all the blocks of the string'''
    
    for smalllist in Tile.TileGroups:
        if smalllist[0] == getstring:
            return smalllist[1]
        
    #If not found
    return -1
def getFlip(getstring):
    '''Receives a group string and returns flip list indexes'''
    for smalllist in Tile.scheduleFlip:
        if smalllist[0] == getstring:
            return Tile.scheduleFlip.index(smalllist)
    return -1
def MoveGroup(block,speed,groupstring,bounds1,bounds2,Horizontal):
    '''Receives a block to update, a group name, pixel boundaries and the block desired speed,
    and a boolean if Horizontal movement or not, intended for easy block movement'''
    
    if block.stringname == groupstring:
        speed = abs(speed)
        if Horizontal:
            if block.rect.left < bounds1:
                Tile.scheduleFlip[getFlip(groupstring)][1] = True
            if block.rect.left > bounds2:
                Tile.scheduleFlip[getFlip(groupstring)][2] = True
        else:
            #Vertical
            if block.rect.top < bounds1:
                Tile.scheduleFlip[getFlip(groupstring)][1] = True
            if block.rect.top > bounds2:
                Tile.scheduleFlip[getFlip(groupstring)][2] = True
            
                    
        if getGroup(groupstring)[ len(getGroup(groupstring)) -1 ] == block:
                if Tile.scheduleFlip[getFlip(groupstring)][1]: #If last block was updated
                    for gblock in getGroup(groupstring):
                        if Horizontal: gblock.xvel = speed
                        else: gblock.yvel = -speed
                    Tile.scheduleFlip[getFlip(groupstring)][1] = False
                    
                elif Tile.scheduleFlip[getFlip(groupstring)][2]:
                    for gblock in getGroup(groupstring):
                        if Horizontal: gblock.xvel = -speed
                        else: gblock.yvel = speed
                    Tile.scheduleFlip[getFlip(groupstring)][2] = False
tsID = {
    'tsDirtTop':0,
    'tsDirt':1,
    'tsDirtL':2,
    'tsDirtR':3,
    'tsDirtLR':4,
    'tsDirtFloat':5,
    'tsDirtFloatL':6,
    'tsDirtFloatR':7,
    'tsGrassFloat':8,
    'tsGrassFloatL':9,
    'tsGrassFloatR':10,
    'tsGrass':11,
    'tsGrassR':12,
    'tsGrassL':13,
    'tsGrownGrass':14,
    'tsMoss':15,
    'tsTriangle':16,
    'tsTriangle':17,
    'tsCrate':18,
    'tsBgTop':19,
    'tsBg':20,
    'tsBgDark':21,
    'tsRocks':22,
    'tsMineral':23,
    'tsShroom':24,
    'tsTree':25,
}
mtsID = {
	'mtsBlock':0,
	'mtsBlockYellow':1,
	'mtsBlockLight':2,
	'mtsBlockWhite':3,
	'mtsBlockRed':4,
	'mtsBars':5,
	'mtsBarsCut':6,
	'mtsBrokenRight':7,
	'mtsBrokenLeft':8,
	'mtsBarsX':9,
	'mtsBarHang':10,
	'mtsBarsBroken':11,
	'mtsSignal':12,
	'mtsBlockMetal':13,
	'mtsTeleporter':14,
	'mtsHotBlock':15,
}

ctsID = {
        'ctsBlock':0,
        'ctsBlockPurple':1,
        'ctsBlockSpot':2,
        'ctsBlockSquare':3,
        'ctsBlockAll':4,
        'ctsBlockRectangle':5,
        'ctsBlockStone':6,
        'ctsBlockCracked':7,
        'ctsBlockBall':8,
        'ctsBlockWhiteDots':9,
        'ctsBlockBlur':10,
        'ctsBlockOrganized':11,
        'ctsBlockShineSpots':12,
        'ctsBlockAllShine':13,
        'ctsBlockSemiShine':14,
        'ctsBlockEyes':15,
        'ctsBlockRectangleEyes':16,
        'ctsBlockRectangleShine':17,
        'ctsBlockRectangleSHine2':18,
        'ctsBlockGiantSquare':19,
        'ctsBlockGiantSquare2':20,
        'ctsBlockWhiteDots2':21,
        'ctsBlockBlurDark':22,
        'ctsBlockSquareDark':23,
        'ctsBlockSquareDarkShine':24,
        'ctsBlockSquareDarkShine2':25,
        'ctsBlockDirty':26,
        
       }
ltsID = {
    
        'ltsBlockL' : 0,
        'ltsBlockCrack' : 1,
        'ltsBlockR' : 2,
        'ltsBlockM':3,
        'ltsBlockMdown':4,
        'ltsBlockLdown':5,
        'ltsBlockRdown':6,
        'ltsBlockBlack':7,
        'ltsBlockML':8,
        'ltsBlockMR':9
        
       } 
class Tile:
    #Stores all tiles images
    Tileset1 = [] 
    Tileset2 = []
    Tileset3 = None
    Tileset4 = None
    TileGroups = []

    scheduleFlip = [['Group1',False,False]]
    
    Tilemap = []
    moveBlocks = []
    fadeBlocks = []
    def __init__(self,x,y,tileset,assetStringname,xvel,yvel,stringname,customPos):
        self.assetStringname = assetStringname
        self.stringname = stringname #For easy reference for special blocks
        self.xvel = xvel
        self.yvel = yvel
        self.x = x
        self.y = y
        if customPos != None: self.x,self.y = customPos
        self.tileset = tileset
        self.width,self.height = (self.tileset).get_rect().size
        self.originalHeight = self.height
        if self.width == 16*27:
            self.rect = pygame.Rect(self.x,self.y,16,16)
            self.Draw = 3
        else:
            self.rect = pygame.Rect(self.x,self.y,self.width, self.height)
            self.Draw = True
            
        if self.stringname != None:
            groupNotCreated = True
            for group in Tile.TileGroups:
                if group[0] == self.stringname:
                    group[1].append(self)
                    groupNotCreated = False
                    break
            if groupNotCreated:
                Tile.TileGroups.append([self.stringname, [self] ])
        
        Tile.Tilemap.append(self)
        #If moving block append to mover blocks list
        if xvel != 0 or yvel != 0: Tile.moveBlocks.append(self)
        if self.stringname != None:
            if 'fadeBlock' in self.stringname: Tile.fadeBlocks.append(self)
        self.fading = False
        self.fadeCounter = 0
        self.respawning = False
            
    def drawtile(self,surface):
        if (self.Draw == True):
            surface.blit(self.tileset,self.rect,(0,0,self.rect.width,self.rect.height))
        elif(self.Draw == 3):
            surface.blit(self.tileset,self.rect,(ctsID[self.assetStringname]*16,0,16,16))
            
    def delete(self):
        Tile.Tilemap.remove(self)
        if self in Tile.moveBlocks: Tile.moveBlocks.remove(self)
        if self in Tile.fadeBlocks: Tile.fadeBlocks.remove(self)
    def fade(self):
        Tile.Tilemap.remove(self)
        self.fading = False
        self.fadeCounter = 0
    def respawn(self):
        Tile.Tilemap.append(self)
        self.fadeCounter = 0
        self.fading = False
        self.respawning = True
    def move(self):
        '''Updates the block position according to its velocity'''
        self.rect.left += self.xvel
        self.rect.top -= self.yvel
    def update(self,gameMap,playerInfo,suddendeath):
        '''Receives the gameMap ID, and list of player rects and their velocities. Updates the Block position every frame, intended for blocks with scripting'''
        #Moving Blocks Code
        self.move() #Updates pos
        if gameMap == 'sandbox':
            if self.stringname == 'testBlock':
                if self.rect.left < 80: self.xvel = 3
                if self.rect.left > 720: self.xvel = -3

        elif gameMap == 3:
            if 'MoveBlocks' in self.stringname:
                if self.rect.top < 20: self.rect.top = GAMEHEIGHT+30
                if suddendeath: self.yvel = 4
        elif gameMap == 4:
            if 'MoveBlocks' in self.stringname:
                if self.rect.top < -32: self.rect.top = GAMEHEIGHT+30
                
            MoveGroup(self,3,'MoveBlocks2',100,500,True)
            MoveGroup(self,3,'MoveBlocks3',780,1180,True)
                
                

           
                
        #Fading block script vanish block
        if self in Tile.fadeBlocks:
            blockActive = self in Tile.Tilemap
            #For single blocks
            if self.stringname == 'fadeBlock': #Single fadeblock
                for playerRect,xvel,yvel in playerInfo:
                    if playerRect.move(0,4).colliderect(self.rect) and yvel > 0 and blockActive and not self.respawning:
                        self.fading = True
            

            #Custom Group Commands
            if self.stringname == 'fadeBlocks1':
                if not self.fading:
                    for playerRect,xvel,yvel in playerInfo:
                        if playerRect.move(0,4).colliderect(self.rect) and yvel > 0 and blockActive and not self.respawning:
                            for block in getGroup('fadeBlocks1'):
                                block.fading = True
                                
            if self.stringname == 'fadeBlocks2':
                if not self.fading:
                    for playerRect,xvel,yvel in playerInfo:
                        if playerRect.move(0,4).colliderect(self.rect) and yvel > 0 and blockActive and not self.respawning:
                            for block in getGroup('fadeBlocks2'):
                                block.fading = True
                    
                
            if self.fading:
                self.fadeCounter +=1
                self.rect.height = self.rect.height*0.99
                if self.fadeCounter == 60 or self.rect.height < 1:
                    self.fade()
            elif not self.fading and not blockActive:
                self.fadeCounter +=1
                if self.fadeCounter == 180:
                    self.respawn()
            elif self.respawning:
                self.rect.height +=1
                if self.rect.height == self.originalHeight:
                    self.respawning = False

            
            
            
                
        
        

class Bg:
    BgAssets = ['tsBg','tsBgDark','tsCrate','tsTriangleR','tsTriangleL','tsGrownGrass','tsMoss','tsRocks','mtsBarsX','mtsSignal',
                'mtsBarsCut','mtsBlockYellow','mtsBarHang','mtsBarsBroken','mtsBars','ctsBlockBlur']
    Bgmap = []
    def __init__(self,x,y,tileset,assetStringname,customPos):
        self.x = x
        self.y = y
        if customPos != None: self.x,self.y = customPos
        self.tileset = tileset
        self.assetStringname = assetStringname 
        self.width,self.height = (self.tileset).get_rect().size
        if self.width == 16*27:
            self.rect = pygame.Rect(self.x,self.y,16,16)
            self.singleDraw = False
        else:
            self.rect = pygame.Rect(self.x,self.y,self.width, self.height)
            self.singleDraw = True
        Bg.Bgmap.append(self)
    def drawtile(self,surface):
        if self.singleDraw:
            surface.blit(self.tileset,self.rect)
        else:
            surface.blit(self.tileset,self.rect,(ctsID[self.assetStringname]*16,0,16,16))
    def delete(self):
        deleter = Bg.Bgmap.index(self)
        del Bg.Bgmap[deleter]
         

def grid(row,column,asset,xvel=0,yvel=0,stringname=None,customPos=None):
    if asset in Bg.BgAssets: isbg = True
    else: isbg = False
    row = row*64
    column = 896-(column+1)*64
    assetStringname = asset
    if asset[0:3] == 'mts':
        assetid = mtsID[asset]
        asset = Tile.Tileset2[assetid]
    elif asset[0:2] == 'ts':
        assetid = tsID[asset]
        asset = Tile.Tileset1[assetid]
    

    if isbg: return Bg(row,column,asset,assetStringname,customPos)
    else: return Tile(row,column,asset,assetStringname,xvel,yvel,stringname,customPos)

def grid16(row,column,asset,xvel=0,yvel=0,stringname=None,customPos=None):
    if asset in Bg.BgAssets: isbg = True
    else: isbg = False
    row = row*16
    column = 896-(column+1)*16
    assetStringname = asset
    asset = Tile.Tileset3
    if isbg: return Bg(row,column,asset,assetStringname,customPos)
    else: return Tile(row,column,asset,assetStringname,xvel,yvel,stringname,customPos)

def grid32(row,column,asset,xvel=0,yvel=0,stringname=None,customPos=None):
    if asset in Bg.BgAssets: isbg = True
    else: isbg = False
    row = row*32
    column = 896-(column+1)*32
    assetStringname = asset
    assetid = ltsID[asset]
    asset = Tile.Tileset4[assetid]
    

    if isbg: return Bg(row,column,asset,assetStringname,customPos)
    else: return Tile(row,column,asset,assetStringname,xvel,yvel,stringname,customPos)
    
'''
#deprecated
def grid32(row,column,asset,xvel=0,yvel=0,stringname=None,customPos=None):
    if asset in Bg.BgAssets: isbg = True
    else: isbg = False
    row = row*32
    column = 896-(column+1)*32
    assetStringname = asset
    asset = Tile.Tileset4
    if isbg: return Bg(row,column,asset,assetStringname,customPos)
    else: return Tile(row,column,asset,assetStringname,xvel,yvel,stringname,customPos)
'''
def LoadMap(newmap):
    bgmap1 = pygame.image.load('Assets/Bgmix.jpg').convert_alpha()
    bgmap2 = pygame.image.load('Assets/Bgmix2.jpg').convert_alpha()
    bgmap3 = pygame.image.load('Assets/Bgmix3.jpg').convert_alpha()
    bgmap4 = pygame.image.load('Assets/Bgmix4.jpg').convert_alpha()
    if newmap == 1:
        exec(open("Maps/map1.txt").read())
        bg = bgmap1
    elif newmap == 2:
        exec(open('Maps/map2.txt').read())
        bg = bgmap2
    elif newmap == 3:
        exec(open('Maps/map3.txt').read())
        bg = bgmap3
    elif newmap == 4:
        exec(open('Maps/map4.txt').read())
        bg = bgmap4
    elif newmap == 'sandbox':
        exec(open('Maps/sandbox.txt').read())
        bg = bgmap2
    Circularity = (xcircular,ycircular)
    return [spawn1,spawn2,xface1,xface2,mapclouds,Circularity,bg,circuitInfo]
    

