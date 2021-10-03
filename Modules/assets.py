import pygame #Import pygame to load images
#Define some colors, to define text easier
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
GOLD = (255, 215, 0)

#Defines all the assets used in-game
def LoadCursor():
    return pygame.image.load('Assets/crosshair.png').convert_alpha()
def LoadBulletAssets():
    bulletasset1 = pygame.image.load('Assets/BulletAssets/bulletplasma.png').convert_alpha()
    bulletasset2 = pygame.image.load('Assets/BulletAssets/bulletplasma2.png').convert_alpha()
    boomerAsset = pygame.image.load('Assets/BulletAssets/boomerangspritesheet.png').convert_alpha()
    boomerAsset = pygame.transform.scale(boomerAsset,(240,30))
    ring0 = pygame.image.load('Assets/BulletAssets/ring/ring0.png').convert_alpha()
    ring1 = pygame.image.load('Assets/BulletAssets/ring/ring1.png').convert_alpha()
    ring2 = pygame.image.load('Assets/BulletAssets/ring/ring2.png').convert_alpha()
    ring3 = pygame.image.load('Assets/BulletAssets/ring/ring3.png').convert_alpha()
    ring4 = pygame.image.load('Assets/BulletAssets/ring/ring4.png').convert_alpha()

    
    wave = [ring0,ring1,ring2,ring3,ring4]
    
    lightBall = pygame.image.load('Assets/BulletAssets/lightball.png').convert_alpha()
    lightBall2 = pygame.image.load('Assets/BulletAssets/lightball2.png').convert_alpha() 
    
    return [bulletasset1,bulletasset2,boomerAsset,wave,lightBall,lightBall2]
def LoadBullet(currWep,playerID,bulletassets):
    '''Receives weapon ID, and player, and returns respective weapon asset'''
    if currWep == 0:
        if playerID == 1: return bulletassets[0]
        else: return bulletassets[1]
    elif currWep == 1:
        return 'laser'
    elif currWep == 2:
        return bulletassets[2]
    elif currWep == 3:
        return bulletassets[3]
    elif currWep == 4:
        if playerID == 1:return bulletassets[4]
        else: return bulletassets[5]
    
def LoadChips():
    returnList = []
    chip1 = pygame.image.load('Assets/WeaponChips/laserChip.png').convert_alpha()
    chip1 = pygame.transform.scale(chip1,(30,30))
    chip2 = pygame.image.load('Assets/WeaponChips/boomerChip.png').convert_alpha() 
    chip2 = pygame.transform.scale(chip2,(30,30))
    chip3 = pygame.image.load('Assets/WeaponChips/waveChip.png').convert_alpha() 
    chip3 = pygame.transform.scale(chip3,(30,30))
    chip4 = pygame.image.load('Assets/WeaponChips/sparkChip.png').convert_alpha() 
    chip4 = pygame.transform.scale(chip4,(30,30))
    
    returnList.extend(['filler',chip1,chip2,chip3,chip4])
    return returnList
def LoadButtonIcons():
    
    plustext = pygame.font.SysFont('FreeSansBold',100).render('+',True,WHITE) #0
    xboxA = pygame.image.load('Assets/MiscButtons/A.png').convert_alpha() #1
    xboxB = pygame.image.load('Assets/MiscButtons/Xbox_X.png').convert_alpha() #2
    xboxRB = pygame.image.load('Assets/MiscButtons/RB.png').convert_alpha() #3
    xboxLB = pygame.image.load('Assets/MiscButtons/LB.png').convert_alpha() #4

    ps4X = pygame.image.load('Assets/MiscButtons/Ps4_X.png').convert_alpha() #5
    ps4Square = pygame.image.load('Assets/MiscButtons/Square.png').convert_alpha() #6
    ps4R1 = pygame.image.load('Assets/MiscButtons/R1.png').convert_alpha() #7 
    ps4L1 = pygame.image.load('Assets/MiscButtons/L1.png').convert_alpha() #8

    q = pygame.image.load('Assets/MiscButtons/q.png').convert_alpha() #9
    w = pygame.image.load('Assets/MiscButtons/w.png').convert_alpha() #10
    e = pygame.image.load('Assets/MiscButtons/e.png').convert_alpha() #11
    space = pygame.image.load('Assets/MiscButtons/space.png').convert_alpha() #12

    endmatchtext = pygame.font.SysFont('FreeSansBold',60).render('To End Match',True,WHITE) #13
    returnList = [plustext,xboxA,xboxB,xboxRB,xboxLB,ps4X,ps4Square,ps4R1,ps4L1,q,w,e,space,endmatchtext]
    return returnList
    
    
    
def LoadMisc():
    returnList = []
    nadeasset = pygame.image.load('Assets/grenade.png').convert_alpha() #0
    cloud1 = pygame.image.load('Tileset/cloud1.png').convert_alpha() #1
    cloud2 = pygame.image.load('Tileset/cloud2.png').convert_alpha() #2
    nadeExplosion = pygame.image.load('Assets/nadeexplosion.png').convert_alpha() #3
    BigLavaLineOn = pygame.image.load('Assets/BigLavaLineOn.png').convert_alpha() #4
    fireRocks = pygame.image.load('Assets/BulletAssets/asteroid.png').convert_alpha() #5
    MenuBg = pygame.image.load('Assets/MenuMix.jpg').convert_alpha() #6
    returnList.extend([nadeasset,cloud1,cloud2,nadeExplosion,BigLavaLineOn,fireRocks,MenuBg])
    return returnList
    
def LoadHUD():
    returnList = []
    wincrown = pygame.image.load('Assets/Crown.png').convert_alpha() #0
    player1pic = pygame.image.load('Assets/hudpic.png').convert_alpha() #1
    healthbar1 = pygame.image.load('Assets/healthbar.png').convert_alpha() #2
    healthbarempty = pygame.image.load('Assets/healthbarempty.png').convert_alpha() #3
    nadebar1 = pygame.image.load('Assets/nadebar.png').convert_alpha() #4
    nadebarempty = pygame.image.load('Assets/emptynadebar.png').convert_alpha() #5

    player2pic = pygame.image.load('Assets/player2/hudpic.png').convert_alpha() #6
    healthbar2 = pygame.image.load('Assets/player2/healthbar.png').convert_alpha() #7
    nadebar2 = pygame.image.load('Assets/player2/nadebar.png').convert_alpha() #8
    nadebarempty2 = pygame.image.load('Assets/player2/emptynadebar.png').convert_alpha() #9
    plasma1 = pygame.image.load('Assets/BulletAssets/bulletplasma.png').convert_alpha() # 10
    plasma2 = pygame.image.load('Assets/BulletAssets/bulletplasma2.png').convert_alpha() #11
    hudgun1 = pygame.image.load('Assets/hudgun1.png').convert_alpha() #12
    hudgun1 = pygame.transform.scale(hudgun1,(50,10))
    hudgun2 = pygame.image.load('Assets/hudgun2.png').convert_alpha() #13
    hudgun2 = pygame.transform.scale(hudgun2,(50,10)) 
    tinystar= pygame.image.load('Assets/tinystar.png').convert_alpha() #14
    tinystar= pygame.transform.scale(tinystar,(15,15))
    #Used plasma for drawing default gun
    laserasset = pygame.image.load('Assets/BulletAssets/laserasset.png').convert_alpha()
    laserasset = pygame.transform.scale(laserasset,(30,3))
    boomerAsset = pygame.image.load('Assets/BulletAssets/boomerasset.png').convert_alpha()
    boomerAsset = pygame.transform.scale(boomerAsset,(20,20))
    waveAsset = pygame.image.load('Assets/BulletAssets/ring/ring4.png').convert_alpha()
    waveAsset = pygame.transform.scale(waveAsset,(10,18))
    lightningAsset = pygame.image.load('Assets/BulletAssets/lightball.png').convert_alpha() 
    specialbulletAssets = ['filler',laserasset,boomerAsset,waveAsset,lightningAsset] #15

    
    returnList.extend([wincrown,player1pic,healthbar1,healthbarempty,nadebar1,nadebarempty,player2pic,healthbar2,
                       nadebar2,nadebarempty2,plasma1,plasma2,hudgun1,hudgun2,tinystar,specialbulletAssets])
    return returnList

    
    
    

#Load Player animations
def LoadSprites(playerID):
    '''Receives if player 1 or 2, and returns a list including all the necessary sprites to draw the player'''
    if playerID == 1:
        returnList = []
        idleleft1 = pygame.image.load('Assets/idleleft.png').convert_alpha()
        idleright1 = pygame.image.load('Assets/idleright.png').convert_alpha()
        idlerightup1 = pygame.image.load('Assets/idlerightup.png').convert_alpha()
        idlerightdown1 = pygame.image.load('Assets/idleleftdown.png').convert_alpha()
        idleleftup1 = pygame.image.load('Assets/idleleftup.png').convert_alpha()
        idleleftdown1 = pygame.image.load('Assets/idlerightdown.png').convert_alpha()
        
        returnList.extend([idleleft1,idleright1,idlerightup1,idlerightdown1,idleleftup1,idleleftdown1])
        
        jumpleft1 = pygame.image.load('Assets/jumpleft.png').convert_alpha()
        jumpright1 = pygame.image.load('Assets/jumpright.png').convert_alpha()
        jumpleftup1 = pygame.image.load('Assets/jumpleftup.png').convert_alpha()
        jumprightup1 = pygame.image.load('Assets/jumprightup.png').convert_alpha()
        jumpleftdown1 = pygame.image.load('Assets/jumpleftdown.png').convert_alpha()
        jumprightdown1 = pygame.image.load('Assets/jumprightdown.png').convert_alpha()
        jumpdownL1 = pygame.image.load('Assets/jumpdownL.png').convert_alpha()
        jumpdownR1 = pygame.image.load('Assets/jumpdownR.png').convert_alpha()
        jumpupL1 = pygame.image.load('Assets/jumpupL.png').convert_alpha()
        jumpupR1 = pygame.image.load('Assets/jumpupR.png').convert_alpha()

        returnList.extend([jumpleft1,jumpright1,jumpleftup1,jumprightup1,jumpleftdown1,jumprightdown1,jumpdownL1,jumpdownR1,jumpupL1,jumpupR1])

        runL1 = pygame.image.load('Assets/spritesheetrunleft.png').convert_alpha()
        runLU1 = pygame.image.load('Assets/spritesheetrunleftup.png').convert_alpha()
        runLD1 = pygame.image.load('Assets/spritesheetrunleftdown.png').convert_alpha()
        runR1 = pygame.image.load('Assets/spritesheetrunright.png').convert_alpha()
        runRU1 = pygame.image.load('Assets/spritesheetrunrightup.png').convert_alpha()
        runRD1 = pygame.image.load('Assets/spritesheetrunrightdown.png').convert_alpha()

        returnList.extend([runL1,runLU1,runLD1,runR1,runRU1,runRD1])

        stillleftdown1 = pygame.image.load('Assets/stillleftdown.png').convert_alpha()
        stillleftup1 = pygame.image.load('Assets/stillleftup.png').convert_alpha()
        stillrightdown1 = pygame.image.load('Assets/stillrightdown.png').convert_alpha()
        stillrightup1 = pygame.image.load('Assets/stillrightup.png').convert_alpha()

        returnList.extend([stillleftdown1,stillleftup1,stillrightdown1,stillrightup1])

    #Player 2
    elif playerID == 2:
        returnList = []
        idleleft2 = pygame.image.load('Assets/player2/idleleft.png').convert_alpha()
        idleright2 = pygame.image.load('Assets/player2/idleright.png').convert_alpha()
        idlerightup2 = pygame.image.load('Assets/player2/idlerightup.png').convert_alpha()
        idlerightdown2 = pygame.image.load('Assets/player2/idleleftdown.png').convert_alpha()
        idleleftup2 = pygame.image.load('Assets/player2/idleleftup.png').convert_alpha()
        idleleftdown2 = pygame.image.load('Assets/player2/idlerightdown.png').convert_alpha()

        returnList.extend([idleleft2,idleright2,idlerightup2,idlerightdown2,idleleftup2,idleleftdown2])

        jumpleft2 = pygame.image.load('Assets/player2/jumpleft.png').convert_alpha()
        jumpright2 = pygame.image.load('Assets/player2/jumpright.png').convert_alpha()
        jumpleftup2 = pygame.image.load('Assets/player2/jumpleftup.png').convert_alpha()
        jumprightup2 = pygame.image.load('Assets/player2/jumprightup.png').convert_alpha()
        jumpleftdown2 = pygame.image.load('Assets/player2/jumpleftdown.png').convert_alpha()
        jumprightdown2 = pygame.image.load('Assets/player2/jumprightdown.png').convert_alpha()
        jumpdownR2 = pygame.image.load('Assets/player2/jumpdownR.png').convert_alpha()
        jumpdownL2 = pygame.image.load('Assets/player2/jumpdownL.png').convert_alpha()
        jumpupL2 = pygame.image.load('Assets/player2/jumpupL.png').convert_alpha()
        jumpupR2 = pygame.image.load('Assets/player2/jumpupR.png').convert_alpha()

        returnList.extend([jumpleft2,jumpright2,jumpleftup2,jumprightup2,jumpleftdown2,jumprightdown2,jumpdownL2,jumpdownR2,jumpupL2,jumpupR2])

        runL2 = pygame.image.load('Assets/player2/spritesheetrunleft.png').convert_alpha()
        runLU2 = pygame.image.load('Assets/player2/spritesheetrunleftup.png').convert_alpha()
        runLD2 = pygame.image.load('Assets/player2/spritesheetrunleftdown.png').convert_alpha()
        runR2= pygame.image.load('Assets/player2/spritesheetrunright.png').convert_alpha()
        runRU2 = pygame.image.load('Assets/player2/spritesheetrunrightup.png').convert_alpha()
        runRD2 = pygame.image.load('Assets/player2/spritesheetrunrightdown.png').convert_alpha()

        returnList.extend([runL2,runLU2,runLD2,runR2,runRU2,runRD2])

        stillleftdown2 = pygame.image.load('Assets/player2/stillleftdown.png').convert_alpha()
        stillleftup2 = pygame.image.load('Assets/player2/stillleftup.png').convert_alpha()
        stillrightdown2 = pygame.image.load('Assets/player2/stillrightdown.png').convert_alpha()
        stillrightup2 = pygame.image.load('Assets/player2/stillrightup.png').convert_alpha()

        returnList.extend([stillleftdown2,stillleftup2,stillrightdown2,stillrightup2])
        
    deathredleft = pygame.image.load('Assets/deathredleft.png').convert_alpha()
    deathredright = pygame.image.load('Assets/deathredright.png').convert_alpha()
    hitleft = pygame.image.load('Assets/hitleft.png').convert_alpha()
    hitright = pygame.image.load('Assets/hitright.png').convert_alpha()
    deathExplosion = pygame.image.load('Assets/deathexplosion.png').convert_alpha() #4
    finaldeathExplosion = pygame.image.load('Assets/finaldeathexplosion.png').convert_alpha() #5


    returnList.extend([deathredleft,deathredright,hitleft,hitright,deathExplosion,finaldeathExplosion])

    return returnList



#Load Tileset ts for short
def LoadTileset():
    Tileset1 = []
    tsDirtTop = pygame.image.load('Tileset/tile_14.png').convert_alpha()
    tsDirt = pygame.image.load('Tileset/tile_04.png').convert_alpha()
    tsDirtL = pygame.image.load('Tileset/tile_03.png').convert_alpha()
    tsDirtR = pygame.image.load('Tileset/tile_05.png').convert_alpha()
    tsDirtLR = pygame.image.load('Tileset/tile_17.png').convert_alpha()
    tsDirtFloat = pygame.image.load('Tileset/tile_09.png').convert_alpha()
    tsDirtFloatL= pygame.image.load('Tileset/tile_58.png').convert_alpha()
    tsDirtFloatR= pygame.image.load('Tileset/tile_18.png').convert_alpha()
    tsGrassFloat = pygame.image.load('Tileset/tile_22.png').convert_alpha()
    tsGrassFloatL= pygame.image.load('Tileset/tile_21.png').convert_alpha()
    tsGrassFloatR= pygame.image.load('Tileset/tile_62.png').convert_alpha()
    tsGrass= pygame.image.load('Tileset/tile_00.png').convert_alpha()
    tsGrassR= pygame.image.load('Tileset/tile_01.png').convert_alpha()
    tsGrassL= pygame.image.load('Tileset/tile_02.png').convert_alpha()
    tsGrownGrass = pygame.image.load('Tileset/tile_28.png').convert_alpha()
    tsMoss = pygame.image.load('Tileset/tile_23.png').convert_alpha()
    tsTriangleL= pygame.image.load('Tileset/tile_20.png').convert_alpha()
    tsTriangleR= pygame.image.load('Tileset/tile_56.png').convert_alpha()
    tsCrate= pygame.image.load('Tileset/tile_06.png').convert_alpha()
    tsBgTop= pygame.image.load('Tileset/tile_13.png').convert_alpha()
    tsBg= pygame.image.load('Tileset/tile_11.png').convert_alpha()
    tsBgDark= pygame.image.load('Tileset/tile_35.png').convert_alpha()
    tsRocks= pygame.image.load('Tileset/tile_46.png').convert_alpha()
    tsMineral= pygame.image.load('Tileset/tile_49.png').convert_alpha()
    tsShroom= pygame.image.load('Tileset/tile_47.png').convert_alpha()
    tsTree = pygame.image.load('Tileset/Tree.png').convert_alpha()
    
    Tileset1.extend([tsDirtTop,tsDirt,tsDirtL,tsDirtR,tsDirtLR,tsDirtFloat,tsDirtFloatL,tsDirtFloatR,tsGrassFloat,tsGrassFloatL,tsGrassFloatR,tsGrass,tsGrassR,tsGrassL,tsGrownGrass,tsMoss,
                     tsTriangleL,tsTriangleR,tsCrate,tsBgTop,tsBg,tsBgDark,tsRocks,tsMineral,tsShroom,tsTree])
    
    #Load Tileset 2 , metal tilset mts for short
    
    Tileset2 = []
    mtsBlock = pygame.image.load('Tileset2/tile1.png').convert_alpha()
    mtsBlockYellow = pygame.image.load('Tileset2/tile2.png').convert_alpha()
    mtsBlockLight = pygame.image.load('Tileset2/tile3.png').convert_alpha()
    mtsBlockWhite = pygame.image.load('Tileset2/tile4.png').convert_alpha()
    mtsBlockRed = pygame.image.load('Tileset2/tile5.png').convert_alpha()
    mtsBars = pygame.image.load('Tileset2/tile6.png').convert_alpha()
    mtsBarsCut = pygame.image.load('Tileset2/tile7.png').convert_alpha()
    mtsBrokenRight = pygame.image.load('Tileset2/tile8.png').convert_alpha()
    mtsBrokenLeft = pygame.image.load('Tileset2/tile9.png').convert_alpha()
    mtsBarsX = pygame.image.load('Tileset2/tile10.png').convert_alpha()
    mtsBarHang = pygame.image.load('Tileset2/tile11.png').convert_alpha()
    mtsBarsBroken = pygame.image.load('Tileset2/tile12.png').convert_alpha()
    mtsSignal = pygame.image.load('Tileset2/tile13.png').convert_alpha()
    mtsBlockMetal = pygame.image.load('Tileset2/tile14.png').convert_alpha()
    mtsTeleporter = pygame.image.load('Tileset2/tile15.png').convert_alpha()
    mtsHotBlock = pygame.image.load('Tileset2/tile16.png').convert_alpha()
    Tileset2.extend([mtsBlock,mtsBlockYellow,mtsBlockLight,mtsBlockWhite,mtsBlockRed,mtsBars,mtsBarsCut,mtsBrokenRight,mtsBrokenLeft,mtsBarsX,mtsBarHang,mtsBarsBroken,
                     mtsSignal,mtsBlockMetal,mtsTeleporter,mtsHotBlock])
    
    Tileset3 = pygame.image.load('Assets/Tileset3.png').convert_alpha()

    Tileset4 = []
    ltsBlockL = pygame.image.load('Tileset4/tile1.png').convert_alpha()
    ltsBlockCrack = pygame.image.load('Tileset4/tile2.png').convert_alpha()
    ltsBlockR = pygame.image.load('Tileset4/tile3.png').convert_alpha()
    ltsBlockM = pygame.image.load('Tileset4/tile4.png').convert_alpha()
    ltsBlockMdown = pygame.image.load('Tileset4/tile5.png').convert_alpha()
    ltsBlockLdown = pygame.image.load('Tileset4/tile6.png').convert_alpha()
    ltsBlockRdown = pygame.image.load('Tileset4/tile7.png').convert_alpha()
    ltsBlockBlack = pygame.image.load('Tileset4/tile8.png').convert_alpha()
    ltsBlockML = pygame.image.load('Tileset4/tile9.png').convert_alpha()
    ltsBlockMR = pygame.image.load('Tileset4/tile10.png').convert_alpha()
    Tileset4.extend([ltsBlockL,ltsBlockCrack,ltsBlockR,ltsBlockM,ltsBlockMdown,ltsBlockLdown,ltsBlockRdown,ltsBlockBlack,
                     ltsBlockML,ltsBlockMR])
    return Tileset1,Tileset2,Tileset3,Tileset4
    

#Generates ALL Game Text
#Pause Menu
def LoadGameFonts():
    gameFont = pygame.font.SysFont('FreeSansBold.ttf',24)
    CLOCKFont = pygame.font.SysFont('FreeSansBold.ttf',50)
    BigFont = pygame.font.SysFont('FreeSansBold.ttf',34)
    MenuFont = pygame.font.SysFont('FreeSansBold',60)
    return gameFont,CLOCKFont,BigFont,MenuFont

def LoadGameText(gameFont,CLOCKFont,BigFont):
    '''Receives Game Fonts, and generates non-changing game text, returns all text as a list'''
    returnList = []
    suddendeathtext = BigFont.render('SUDDEN DEATH!',True,RED,BLACK) #0
    ResumePauseMenuText = CLOCKFont.render('Resume',True,GOLD).convert_alpha() #1
    Counter3 = CLOCKFont.render('3...',True,GOLD) #2
    Counter2 = CLOCKFont.render('2...',True,GOLD) #3
    Counter1 = CLOCKFont.render('1...',True,GOLD) #4
    StartCounter = CLOCKFont.render('Start!',True,GOLD) #5
    tieText = CLOCKFont.render('Tie!',True,RED) #6
    win1Text = CLOCKFont.render('PLAYER 2 WINS!',True,RED) #7
    win2Text = CLOCKFont.render('PLAYER 1 WINS!',True,RED) #8
    returnList.extend([suddendeathtext,ResumePauseMenuText,Counter3,Counter2,Counter1,StartCounter,tieText,win1Text,win2Text])
    return returnList

def LoadMenuText(MenuFont,CLOCKFont):
    returnList = []
    ZeroSubFighttext = pygame.font.SysFont('timesnewroman',100).render('ZEROSUB FIGHT',True,GOLD) #0

    Playtext = MenuFont.render('Play',True,WHITE) #1
    PlaytextActive = MenuFont.render('Play',True,GOLD) #2
    Optionstext = MenuFont.render('Settings',True,WHITE) #3
    OptionstextActive = MenuFont.render('Settings',True,GOLD) #4
    Exitgametext = MenuFont.render('Exit Game',True,WHITE) #5
    ExitgametextActive = MenuFont.render('Exit Game',True,GOLD) #6
    #Settings
    MusicVolumetext = MenuFont.render('Music Volume: ',True,WHITE) #7
    MusicVolumetextActive = MenuFont.render('Music Volume: ',True,GOLD) #8
    SFXVolumetext = MenuFont.render('SFX Volume: ',True,WHITE) #9
    SFXVolumetextActive = MenuFont.render('SFX Volume: ',True,GOLD) #10
    Mutetext = MenuFont.render('Mute: ',True,WHITE) #11
    MutetextActive = MenuFont.render('Mute: ',True,GOLD) #12
    
    Backtext = MenuFont.render('Back',True,WHITE) #13
    BacktextActive = MenuFont.render('Back',True,GOLD) #14
    Randomtext = CLOCKFont.render('Random',True,RED) #15
    map1text = CLOCKFont.render('Forest',True,WHITE) #16
    map2text = CLOCKFont.render('City',True,WHITE) #17
    map3text = CLOCKFont.render('Outskirts',True,WHITE) #18
    map4text = CLOCKFont.render('Volcano',True,WHITE) #19

    bigplaytext = MenuFont.render('PLAY!',True,GOLD) #20

    
    returnList.extend([ZeroSubFighttext,Playtext,PlaytextActive,Optionstext,OptionstextActive,Exitgametext,ExitgametextActive,
                       MusicVolumetext,MusicVolumetextActive,SFXVolumetext,SFXVolumetextActive,Mutetext,MutetextActive,
                       Backtext,BacktextActive,Randomtext,map1text,map2text,map3text,map4text,bigplaytext])
    return returnList


def LoadThumbnails():
    map1 = pygame.image.load('Assets/MapThumbnails/map1.jpg').convert_alpha()
    map1 = pygame.transform.scale(map1,(300,200))
    
    map2 = pygame.image.load('Assets/MapThumbnails/map2.jpg').convert_alpha()
    map2 = pygame.transform.scale(map2,(300,200))
    
    map3 = pygame.image.load('Assets/MapThumbnails/map3.jpg').convert_alpha()
    map3 = pygame.transform.scale(map3,(300,200))
    
    map4 = pygame.image.load('Assets/MapThumbnails/map4.jpg').convert_alpha()
    map4 = pygame.transform.scale(map4,(300,200))

    random = pygame.image.load('Assets/MapThumbnails/random.jpg').convert_alpha()
    random = pygame.transform.scale(random,(200,133))
    returnList = [map1,map2,map3,map4,random]
    return returnList
    



