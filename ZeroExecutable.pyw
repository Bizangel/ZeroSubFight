import pygame
from random import randint
from collections import namedtuple
# Only import functions we use
from weaponry import *
from playerDefs import *
from gameControls import *
from SoundEffects import *
from tileinfo import *  # This includes assets.py
from Modules.Sketches import *  # Drawing defs
from Modules.extraFunctions import generatePoints


def GameValues():
    ''' Resets all the Game Values to their Default Values, done on each map load, returns these values'''
    GAMEWIDTH = 1280
    # We use globals because we're inside a function and want to keep all of these throughout the game.
    suddendeath = False
    cloudx1 = GAMEWIDTH + 50
    cloudx2 = GAMEWIDTH + 150
    cloudy1 = randint(0, 400)
    cloudy2 = randint(0, 400)
    mapTimer = 0
    lavaUp = True
    lavaID = 0
    suddendeathClock = 0
    postmapTimer = 0
    premapTimer = 0
    canPause = False
    GamePause = True
    cloudsInfo = [[cloudx1, cloudy1], [cloudx2, cloudy2]]
    Timers = [premapTimer, mapTimer, postmapTimer, suddendeathClock]
    LavaInfo = [lavaUp, lavaID]
    currentChip = 0
    return [Timers, cloudsInfo, LavaInfo, suddendeath, canPause, GamePause, currentChip]


def MapRestart(newmap, player1, player2):
    ''' Receives the map to be loaded, and sets everything in the game to be ready for a new match in a different map'''

    MusicList = ['Sounds/menumusic.mp3', 'Sounds/forest.wav',
                 'Sounds/city.mp3', 'Sounds/outskirts.wav', 'Sounds/volcano.wav']
    for tile in Tile.Tilemap:
        tile.delete()
    for bg in Bg.Bgmap:
        bg.delete()

    # Ensure a new map and reset everything
    Tile.Tilemap = []
    Tile.moveBlocks = []
    Tile.fadeBlocks = []
    Bullet.Bullets1 = []
    Bullet.Bullets2 = []
    Bullet.Lightnings1 = [0, [], 0]
    Bullet.Lightnings2 = [0, [], 0]
    Bg.Bgmap = []
    tileHitbox = []
    Hazard.Hazards = []
    SmallParticles.Particles = []
    WeaponChip.chips = []

    # Loads corresponding map and sets background of it
    MapInfo = LoadMap(newmap)
    # Creates our new tileHitbox according to the map
    for tile in Tile.Tilemap:
        tileHitbox.append(tile.rect)
    GameValues()  # Resets the Game Values
    # Reset player Values
    player1.Reset(MapInfo[0], MapInfo[2])
    player2.Reset(MapInfo[1], MapInfo[3])

    # sets music
    pygame.mixer.music.stop()
    pygame.mixer.music.load(MusicList[newmap])
    pygame.mixer.music.play(-1)
    return MapInfo, tileHitbox


def main():
    '''Main function, run at start, runs the game'''
    devMode = False
    windowresize = False
    # Initializes pygame module, allowing to load images create windows, surfaces etc.
    pygame.init()
    # define list that will keep track of music

    # Define some colors for later use
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    GOLD = (255, 215, 0)
    ORANGE = (252, 126, 36)
    GREY = (59, 60, 82)
    YELLOW = (211, 228, 25)

    # Sets Mapheight, gamewidth and gameheight, NOT supposed to be changed.
    MAPHEIGHT = 896
    GAMEWIDTH = 1280
    GAMEHEIGHT = 964
    # Choose map randomly, from all available maps
    nMaps = 4  # Sets number of in-game Maps
    nChips = 3  # Defines number of weapon chips

    gameMap = randint(1, nMaps)
    #gameMap = 4

    # If window resize is enabled, everything will be created on displaysurf, then at the end resized to the displayed window surface called 'window'
    if not windowresize:
        displaysurf = pygame.display.set_mode((GAMEWIDTH, GAMEHEIGHT))
    # defines PauseSurface, which will be shown when paused.
    PauseSurface = pygame.Surface([GAMEWIDTH, GAMEHEIGHT])
    # If Different Resolution
    # Set Y, sets x based on side because new window has to keep aspect ratio from original window.
    if windowresize:
        windowy = 680
        windowx = round(GAMEWIDTH/GAMEHEIGHT*windowy)
        displaysurf = pygame.Surface([GAMEWIDTH, GAMEHEIGHT])
        window = pygame.display.set_mode([windowx, windowy])

    # Loads Tileset
    Tile.Tileset1, Tile.Tileset2, Tile.Tileset3, Tile.Tileset4 = LoadTileset()
    MapInfo = LoadMap(gameMap)  # Loads Map
    bg = MapInfo[6]
    tileHitbox = []
    # Gets tilehitbox, which our game will use to know WHAT counts as a physical block and what is NOT a physical block(background)
    for tile in Tile.Tilemap:
        tileHitbox.append(tile.rect)

    # Loads Misc Assets, Load Game Fonts
    chipAssets = LoadChips()
    MiscAssets = LoadMisc()
    gameFont, CLOCKFont, BigFont, MenuFont = LoadGameFonts()
    GameTexts = LoadGameText(gameFont, CLOCKFont, BigFont)
    MenuTexts = LoadMenuText(MenuFont, CLOCKFont)
    MapThumbnails = LoadThumbnails()
    BulletAssets = LoadBulletAssets()
    ButtonIcons = LoadButtonIcons()
    SoundEffects = LoadSFX()

    # Creates Each Necessary Object, The players and their respective nades. Each one with their respective asset to be drawn initially
    # Their spawnlocations are determined depending on the map, (See each maps .txt file)
    grenade1 = Grenade(0, 0, MiscAssets[0], MiscAssets[3], SoundEffects[5])
    player1 = Player(MapInfo[0], MapInfo[2], LoadSprites(1), grenade1,
                     'player1', [SoundEffects[6], SoundEffects[7]])
    grenade2 = Grenade(0, 0, MiscAssets[0], MiscAssets[3], SoundEffects[5])
    player2 = Player(MapInfo[1], MapInfo[3], LoadSprites(2), grenade2,
                     'player2', [SoundEffects[6], SoundEffects[7]])
    Player.Players.append(player1)
    Player.Players.append(player2)
    # Appends the players to a list of players for easy tracking of them.

    # Sets Game Values
    # We set our values initially for the first map load.
    Timers, cloudsInfo, LavaInfo, suddendeath, canPause, GamePause, currentChip = GameValues()  # Loads GameValues

    # We define our namedtuple which is very convenient for movement management.
    Move = namedtuple('move', ['up', 'left', 'right'])
    pointlist = generatePoints((0, 5), (GAMEWIDTH-5, 5))  # creates initial pointlist for map3
    # Starts Joysticks
    pygame.joystick.init()
    getJoys = pygame.joystick.get_count()  # Gets How many controllers are plugged to start them
    if getJoys == 0:
        pass  # Does not start anything
    elif getJoys == 1:  # Starts the single joystick
        joystick1 = pygame.joystick.Joystick(0)
        joystick1.init()
    elif getJoys == 2:  # Starts both joysticks
        joystick1 = pygame.joystick.Joystick(0)
        joystick2 = pygame.joystick.Joystick(1)
        joystick1.init()
        joystick2.init()

    if getJoys < 2:
        player1.mouseTrack = True
    if getJoys == 0:
        player2.no360 = True
    # Game Map Restarts
    HUDAssets = LoadHUD()  # Load HUD Assets
    pygame.display.set_caption('ZeroSub Fight')  # Sets the Caption Display of the Game
    clock = pygame.time.Clock()  # Creates a clock object which will regulate our in-game FPS

    frame_counter = 0
    # Main Loop
    # Define our run boolean variable, which we will turn off when the user decides to quit
    run = True
    debug = False
    # Menu Variables
    gameGo = False
    MenuBgPos = 0
    MenuPos = -1
    MenuPlay, MenuSettings = False, False
    PreAction = False
    MenuAccelTimer = 0
    AccelerationCounter = 0
    Endless = True
    runMap = 0
    MusicVolume = 100
    #MusicVolume = 0
    SFXVolume = 100
    MenuCoords = [0, 0]
    Mute = False  # Game Muted
    MenuActionDone = False
    MenuGraceTimer = 0
    menuBreak = False
    spedup = False
    pygame.mixer.music.load('Sounds/menumusic.mp3')
    pygame.mixer.music.play(-1)

    # Sets custom game cursor and disables usual one
    gameCursor = LoadCursor()
    cursorRect = pygame.Rect((0, 0), gameCursor.get_size())
    onMenu = True
    while run:
        # Set FPS
        clock.tick_busy_loop(60)
        # updates music to volume
        if not Mute:
            realVolume = MusicVolume/100
            realSFX = SFXVolume/100
        else:
            realVolume = 0
            realSFX = 0

        pygame.mixer.music.set_volume(realVolume)
        if onMenu:
            # Ensures SFX correct Volume
            for SFX in SoundEffects:
                SFX.set_volume(realSFX)
            '''Menu Display and Code'''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if devMode:
                        if event.key == pygame.K_p:
                            run = False
                        elif event.key == pygame.K_m:
                            Mute = True
            PreAction = False

            if not MenuActionDone:
                MenuAccelTimer += 1
                if MenuAccelTimer > 15:
                    AccelerationCounter = 0
            if MenuActionDone:
                MenuGraceTimer += 1
                if MenuGraceTimer > 10:
                    MenuGraceTimer = 0
                    MenuActionDone = False
                    PreAction = True
                    AccelerationCounter += 1

            if getJoys < 1 and not MenuActionDone:
                MenuPos, MenuPlay, MenuSettings, MusicVolume, SFXVolume, run, MenuActionDone, Mute, spedup, onMenu, MenuCoords, Endless, runMap, gameGo = MenuControls(MenuPos, [MenuPlay, MenuSettings, MusicVolume, SFXVolume, run,
                                                                                                                                                                                 MenuGraceTimer, Mute, spedup, MenuCoords, Endless, runMap, gameGo], SoundEffects)
            elif not MenuActionDone:
                MenuPos, MenuPlay, MenuSettings, MusicVolume, SFXVolume, run, MenuActionDone, Mute, spedup, onMenu, MenuCoords, Endless, runMap, gameGo = MenuControls(MenuPos, [MenuPlay, MenuSettings, MusicVolume, SFXVolume, run,
                                                                                                                                                                                 MenuGraceTimer, Mute, spedup, MenuCoords, Endless, runMap, gameGo], SoundEffects, joystick1)

            if PreAction and MenuActionDone and AccelerationCounter > 6:
                spedup, AccelerationCounter = True, 0

            MenuBgPos -= 1
            displaysurf.blit(MiscAssets[6], (MenuBgPos, -28))  # fill in with bg
            displaysurf.blit(MiscAssets[6], (MenuBgPos+8192, -28))
            if MenuBgPos < -8192:
                MenuBgPos = 0
            if not MenuPlay:
                displaysurf.blit(MenuTexts[0], (250, 100))  # Game Logo
            # Update activeID
            ActiveID = [0, 0, 0, 0]
            if MenuPos != -1:
                ActiveID[MenuPos] = 1
            # Display Main menu
            if not MenuPlay and not MenuSettings:

                displaysurf.blit(MenuTexts[1+ActiveID[0]], (GAMEWIDTH/2-60, 300))
                displaysurf.blit(MenuTexts[3+ActiveID[1]], (GAMEWIDTH/2-100, 500))
                displaysurf.blit(MenuTexts[5+ActiveID[2]], (GAMEWIDTH/2-120, 700))
            # Display when MenuSettings

            elif MenuSettings:
                MusicInt = CLOCKFont.render('{0}'.format(MusicVolume), True, WHITE)
                SFXInt = CLOCKFont.render('{0}'.format(SFXVolume), True, WHITE)
                if Mute:
                    MutedText = 'ON'
                else:
                    MutedText = 'OFF'
                MuteText = CLOCKFont.render(MutedText, True, RED)
                displaysurf.blit(MusicInt, (790, 312))
                displaysurf.blit(SFXInt, (790, 410))
                displaysurf.blit(MuteText, (550, 505))
                MusicRect = pygame.Rect(570, 310, MusicVolume*2, 30)
                SFXRect = pygame.Rect(570, 410, SFXVolume*2, 30)
                if MusicVolume > 0:
                    pygame.draw.rect(displaysurf, GREY, MusicRect)
                if SFXVolume > 0:
                    pygame.draw.rect(displaysurf, GREY, SFXRect)
                pygame.draw.rect(displaysurf, BLACK, (570, 310, 200, 30), 3)
                pygame.draw.rect(displaysurf, BLACK, (570, 410, 200, 30), 3)
                displaysurf.blit(MenuTexts[7+ActiveID[0]], (GAMEWIDTH/2-400, 300))
                displaysurf.blit(MenuTexts[9+ActiveID[1]], (GAMEWIDTH/2-360, 400))
                displaysurf.blit(MenuTexts[11+ActiveID[2]], (GAMEWIDTH/2-225, 500))
                displaysurf.blit(MenuTexts[13+ActiveID[3]], (GAMEWIDTH/2-100, 620))
            elif MenuPlay:
                mapRects = [(300, 50, 200, 133), (300, 250, 300, 200), (650, 250, 300, 200),
                            (300, 500, 300, 200), (650, 500, 300, 200)]  # from 0 to 4 0 being random
                rects = [[(300, 50, 200, 133), (300, 250, 300, 200), (300, 500, 300, 200), (550, 800, 120, 38)], [
                    (-100, -100, 0, 0), (650, 250, 300, 200), (650, 500, 300, 200), (550, 800, 120, 38)]]
                if MenuCoords == [1, 0]:
                    endlessColor = YELLOW
                else:
                    endlessColor = WHITE
                if Endless:
                    endlesstext = MenuFont.render('Endless', True, endlessColor)
                else:
                    endlesstext = MenuFont.render('Single Match', True, endlessColor)

                displaysurf.blit(MapThumbnails[0], (300, 250))
                displaysurf.blit(MapThumbnails[1], (650, 250))
                displaysurf.blit(MapThumbnails[2], (300, 500))
                displaysurf.blit(MapThumbnails[3], (650, 500))

                displaysurf.blit(MapThumbnails[4], (300, 50))
                displaysurf.blit(MenuTexts[15], (330, 105))  # "random" text

                if MenuCoords == [0, 3] or MenuCoords == [1, 3]:
                    pygame.draw.rect(displaysurf, RED, rects[MenuCoords[0]][MenuCoords[1]])
                else:
                    pygame.draw.rect(displaysurf, YELLOW, rects[MenuCoords[0]][MenuCoords[1]], 5)
                pygame.draw.rect(displaysurf, RED, mapRects[runMap], 3)

                displaysurf.blit(MenuTexts[16], (405, 450))
                displaysurf.blit(MenuTexts[17], (755, 450))
                displaysurf.blit(MenuTexts[18], (385, 700))
                displaysurf.blit(MenuTexts[19], (735, 700))
                displaysurf.blit(MenuTexts[20], (550, 800))

                displaysurf.blit(endlesstext, (700, 100))
                if gameGo:  # Ready to load
                    if runMap != 0:
                        gameMap = runMap
                    else:
                        gameMap = randint(1, nMaps)
                    MapInfo, tileHitbox = MapRestart(gameMap, player1, player2)
                    bg = MapInfo[6]
                    Timers, cloudsInfo, LavaInfo, suddendeath, canPause, GamePause, currentChip = GameValues()
                    gameGo = False

            if windowresize:
                frame = pygame.transform.scale(displaysurf, (windowx, windowy))
                window.blit(frame, frame.get_rect())

            pygame.display.update()

            continue  # skips the whole loop and only stays on Menu

        '''Game Code and Actual Gameplay'''

        if getJoys < 2:
            pygame.mouse.set_visible(False)
        frame_counter += 1
        # If map hasn't started
        if Timers[1] < 60:
            Timers[0] += 1
        if Timers[0] > 180:
            GamePause = False
        if Timers[0] == 240:
            Timers[0], canPause, player1.pause, player2.pause = 0, True, False, False
        # Game Map Timer 3M, 10800 frames equals 3m
        if Timers[1] >= 10800:
            suddendeath = True
        # If a player has lost, start postgame timer
        if player1.hp == 0 or player2.hp == 0:
            canPause = False  # disable pause at end
        if (player1.win and player1.hp == 0) or (player2.win and player2.hp == 0):
            pygame.mixer.music.stop()  # stop music
        if not player1.win or not player2.win:
            Timers[2] += 1
        if not GamePause:
            Timers[1] += 1  # If game not paused, tick the map Timer
        MapMinutes = 2 - Timers[1] // 3600  # Define the counter minutes, to display on the clock
        MapSeconds = 60 - (Timers[1]//60) % 60  # Define the counter seconds, to display on the cock
        # If Sudden Death Start Deleting Tiles, Use suddendeathClock, 120frames = 2s
        if gameMap != 3:
            deleteTimer = 90
        else:
            deleteTimer = 2
        if suddendeath:
            if not GamePause:
                Timers[3] += 1
            if Timers[3] > deleteTimer:
                if len(Tile.Tilemap) > 0:
                    Tile.Tilemap[randint(0, len(Tile.Tilemap)-1)].delete()
                if len(Bg.Bgmap) > 0:
                    Bg.Bgmap[randint(0, len(Bg.Bgmap)-1)].delete()
                Timers[3] = 0

        # Keybinds Events, for singletime Press Controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                '''
                ########################
                ### DEVMODE COMMANDS ###
                ########################
                '''
                if devMode:
                    if event.key == pygame.K_p:
                        run = False
                    elif event.key == pygame.K_1:
                        gameMap = 1
                        MapInfo, tileHitbox = MapRestart(gameMap, player1, player2)
                        bg = MapInfo[6]
                        Timers, cloudsInfo, LavaInfo, suddendeath, canPause, GamePause, currentChip = GameValues()
                    elif event.key == pygame.K_2:
                        gameMap = 2
                        MapInfo, tileHitbox = MapRestart(gameMap, player1, player2)
                        bg = MapInfo[6]
                        Timers, cloudsInfo, LavaInfo, suddendeath, canPause, GamePause, currentChip = GameValues()
                    elif event.key == pygame.K_3:
                        gameMap = 3
                        MapInfo, tileHitbox = MapRestart(gameMap, player1, player2)
                        bg = MapInfo[6]
                        Timers, cloudsInfo, LavaInfo, suddendeath, canPause, GamePause, currentChip = GameValues()
                    elif event.key == pygame.K_4:
                        gameMap = 4
                        MapInfo, tileHitbox = MapRestart(gameMap, player1, player2)
                        bg = MapInfo[6]
                        Timers, cloudsInfo, LavaInfo, suddendeath, canPause, GamePause, currentChip = GameValues()
                    elif event.key == pygame.K_5:
                        if GamePause and canPause:
                            GamePause = False
                        elif canPause:
                            GamePause = True
                    elif event.key == pygame.K_7:
                        suddendeath = True

                    elif event.key == pygame.K_6:
                        WeaponChip(MapInfo[7][0], chipAssets[4], 4)
                        SoundEffects[4].play()
                    elif event.key == pygame.K_r:
                        if debug:
                            debug = False
                            print('DEBUG OFF')
                        else:
                            debug = True
                            print('DEBUG ON')
                    elif event.key == pygame.K_u:
                        exec(open("debugCommands.txt").read())

        # Updates cursor rect wether paused or not
        cursorRect.centerx, cursorRect.centery = pygame.mouse.get_pos()
        if windowresize:
            cursorRect.centerx *= GAMEWIDTH/windowx
            cursorRect.centery *= GAMEHEIGHT/windowy
        # Updates GamePause
        if getJoys == 0:
            menuBreak = PauseControls(canPause, player1, GamePause, menuBreak)
            # menuBreak = PauseControls(canPause,player2,GamePause,menuBreak) only player1 can pause
        elif getJoys == 1:
            menuBreak = PauseControls(canPause, player1, GamePause, menuBreak)
            menuBreak = PauseControls(canPause, player2, GamePause, menuBreak, joystick1)
        elif getJoys == 2:
            menuBreak = PauseControls(canPause, player1, GamePause, menuBreak, joystick1)
            menuBreak = PauseControls(canPause, player2, GamePause, menuBreak, joystick2)
        for player in Player.Players:
            if player.recentlyPaused:
                player.pauseCounter += 1
                if player.pauseCounter > 15:
                    player.pauseCounter = 0
                    player.recentlyPaused = False

        if player1.pause and player2.pause:
            player1.pause, player2.pause = True, False  # in rare case they pause at same time

        if canPause:
            GamePause = (player1.pause or player2.pause)  # if one of them has paused
        if GamePause:
            pass  # Do nothing
        # If not Paused, use normal GameControls and update everyone's state.
        if not GamePause:
            if getJoys == 0:
                GameControls(player1, LoadBullet(player1.currentWeapon, 1, BulletAssets))
                GameControls(player2, LoadBullet(player2.currentWeapon, 2, BulletAssets))
            elif getJoys == 1:
                GameControls(player1, LoadBullet(player1.currentWeapon, 1, BulletAssets))
                GameControls(player2, LoadBullet(player2.currentWeapon, 2, BulletAssets), joystick1)
            elif getJoys == 2:
                GameControls(player1, LoadBullet(player1.currentWeapon, 1, BulletAssets), joystick2)
                GameControls(player2, LoadBullet(player2.currentWeapon, 2, BulletAssets), joystick1)

            # Updates P1 and P2 (Position, shoot, grenades, animations, overheats etc.)
            for player in Player.Players:
                player.update(player.move, Tile.Tilemap, Tile.moveBlocks, Tile.Tilemap, tileHitbox, [player1, player2],
                              suddendeath, MapInfo[5], gameMap, cursorRect)
            # Update P1 and P2 bullets and lightballs
            for bullet in Bullet.Bullets1:
                bullet.update(player1, player1, player2, tileHitbox, Tile.moveBlocks)
            for bullet in Bullet.Bullets2:
                bullet.update(player2, player1, player2, tileHitbox, Tile.moveBlocks)

            for lightball in Bullet.Lightnings1[1]:
                lightball.update(player1, player1, player2, tileHitbox, Tile.moveBlocks)
            for lightball in Bullet.Lightnings2[1]:
                lightball.update(player2, player1, player2, tileHitbox, Tile.moveBlocks)

            for chip in WeaponChip.chips:
                chip.update()

            # Updates pointlist lightning map3
            if gameMap == 3:
                pointlist = generatePoints((0, 5), (GAMEWIDTH-5, 5))
            # Updates particles
            for particle in SmallParticles.Particles:
                particle.update(player1, player2)

            # Create Hazard every once in a while
            if suddendeath:
                meteorTime = 10
            else:
                meteorTime = 100
            if Timers[1] % meteorTime == 0 and gameMap == 4:
                Hazard(randint(30, GAMEWIDTH-30), 0, randint(-3, 3), -10, MiscAssets[5])
                Hazard(randint(30, GAMEWIDTH-30), 0, randint(-3, 3), -10, MiscAssets[5])
                Hazard(randint(30, GAMEWIDTH-30), 0, randint(-3, 3), -10, MiscAssets[5])
            # Update hazard
            for hazard in Hazard.Hazards:
                hazard.update(player1, player2, tileHitbox)
            # Updates Clouds x position
            cloudsInfo[0][0] -= 0.5
            cloudsInfo[1][0] -= 1
            if cloudsInfo[0][0] < -220:
                cloudsInfo[0][0] = GAMEWIDTH + 200
                cloudsInfo[0][1] = randint(0, 400)
            if cloudsInfo[1][0] < -150:
                cloudsInfo[1][0] = GAMEWIDTH + 400
                cloudsInfo[1][1] = randint(0, 400)
            # Updates Blocks Positions
            for block in Tile.moveBlocks:
                block.update(gameMap, [(player1.rect, player1.xvel, player1.yvel),
                                       (player2.rect, player2.xvel, player2.yvel)], suddendeath)
            for block in Tile.fadeBlocks:
                block.update(gameMap, [(player1.rect, player1.xvel, player1.yvel),
                                       (player2.rect, player2.xvel, player2.yvel)], suddendeath)

            # Updates Tile Hitbox
            tileHitbox = []
            for tile in Tile.Tilemap:
                tileHitbox.append(tile.rect)

            if currentChip <= 11:
                if MapInfo[7][-1][currentChip] == -1 and currentChip < 11:
                    currentChip += 1  # Skips to next chip if no chip was generated

                # Gets Chip List, Last Element List which contains the timers
                if Timers[1] == MapInfo[7][-1][currentChip]:
                    chooser = randint(0, len(MapInfo[7])-2)
                    spawnchip = randint(1, nChips)
                    WeaponChip(MapInfo[7][chooser], chipAssets[spawnchip], spawnchip)
                    currentChip += 1
                    SoundEffects[4].play()

            # Activates chis on player contact
            for player in Player.Players:
                chipRects = [chip.rect for chip in WeaponChip.chips]
                chipCollideIndex = player.rect.collidelist(chipRects)
                if chipCollideIndex != -1:
                    WeaponChip.chips[chipCollideIndex].activate(player)
                    SoundEffects[3].play()
                    break

        # If match just ended
        if Timers[2] == 10:
            pygame.mixer.music.load('Sounds/matchEnd.wav')
            pygame.mixer.music.play(0)
        # Makes New Map and reset after 300 frames(5s) of match End
        # Map random choosal
        if Timers[2] > 300 and Endless:
            oldgameMap = gameMap
            if not (player1.win or player2.win):
                pass  # Tie
            elif not player1.win:
                player2.Wins += 1
            elif not player2.win:
                player1.Wins += 1
            while gameMap == oldgameMap:  # To avoid same map repeating
                gameMap = randint(1, nMaps)
            MapInfo, tileHitbox = MapRestart(gameMap, player1, player2)
            bg = MapInfo[6]
            Timers, cloudsInfo, LavaInfo, suddendeath, canPause, GamePause, currentChip = GameValues()  # Resets Game Values
            menuBreak = False
            MenuCoords = [0, 0]
        elif Timers[2] > 300 and not Endless:  # not endless send back to Map Menu
            onMenu = True
            menuBreak = False
            MenuPlay, MenuSettings = True, False
            runMap = 0
            MenuCoords = [0, 0]
            # reset music
            pygame.mixer.music.stop()
            pygame.mixer.music.load('Sounds/menumusic.mp3')
            pygame.mixer.music.play(-1)
        elif menuBreak:
            onMenu = True
            menuBreak = False
            MenuPlay, MenuSettings = True, False
            runMap = 0
            MenuCoords = [0, 0]
            # reset music
            pygame.mixer.music.stop()
            pygame.mixer.music.load('Sounds/menumusic.mp3')
            pygame.mixer.music.play(-1)

        # Render texts
        clocktext = CLOCKFont.render('{0}:{1:02d}'.format(
            MapMinutes, MapSeconds), True, (252, 126, 36), BLACK)
        hptext1 = gameFont.render('HP {0}/300'.format(player1.hp), True, RED, BLACK)
        hptext2 = gameFont.render('HP {0}/300'.format(player2.hp), True, ORANGE, BLACK)
        wintext1 = gameFont.render(':{0}'.format(player1.Wins), True, GOLD, BLACK)
        wintext2 = gameFont.render(':{0}'.format(player2.Wins), True, GOLD, BLACK)

        ''' Redraws and updates the entire screen '''

        # Remember, everything drawn is drawn on top of everything that was drawn before.
        # Reloads Background, taking over everything previously drawn on the screen
        displaysurf.blit(bg, (0, 0))
        # Draw Clouds
        if MapInfo[4]:  # If it's a map that uses clouds.
            displaysurf.blit(MiscAssets[1], cloudsInfo[0])
            displaysurf.blit(MiscAssets[2], cloudsInfo[1])
        # Draws background
        for tile in Bg.Bgmap:
            tile.drawtile(displaysurf)
        # Draws Foreground
        for tile in Tile.Tilemap:
            tile.drawtile(displaysurf)

        # Draw Player1 and Player2 accordingly
        for player in Player.Players:
            player.rect.left -= 8
            player.Draw(displaysurf)
            player.rect.right += 8
        # Draw Nades
        for player in Player.Players:
            player.drawNade(displaysurf)

        # Draws wep Chips
        for chip in WeaponChip.chips:
            chip.draw(displaysurf)
        # Draws the bullets from each player.
        for bullet in Bullet.Bullets1:
            bullet.draw(displaysurf)
        for bullet in Bullet.Bullets2:
            bullet.draw(displaysurf)
        # draw lightnings
        for lightning in Bullet.Lightnings1[1]:
            lightning.draw(displaysurf)
        for lightning in Bullet.Lightnings2[1]:
            lightning.draw(displaysurf)
        # Update lightnings
        Bullet.Lightnings1[2] += 1
        Bullet.Lightnings2[2] += 1

        if gameMap == 3:
            pygame.draw.lines(displaysurf, (166, 188, 79), False,
                              pointlist, 3)  # draw map3 lightning

        # draw small effects
        for particle in SmallParticles.Particles:
            particle.draw(displaysurf)
        # draw hazard, meteorites
        for hazard in Hazard.Hazards:
            hazard.draw(displaysurf)

        DrawHUD(displaysurf, HUDAssets, chipAssets, [hptext1, hptext2, wintext1, wintext2],
                [(player1.hp, player1.nadeCDTimer, player1.overheatCounter, player1.currentWeapon, player1.weaponTimer, player1.Wins),
                 (player2.hp, player2.nadeCDTimer, player2.overheatCounter, player2.currentWeapon, player2.weaponTimer, player2.Wins)])  # Redraws HUD

        # Display Clock or Sudden Death Text/Lava
        if not suddendeath:
            displaysurf.blit(clocktext, (GAMEWIDTH/2-30, MAPHEIGHT+20))
        else:
            LavaInfo = DrawSuddenDeath(displaysurf, LavaInfo, GameTexts[0], MiscAssets[4])

        # If both players have lost, draw Tie!
        if not player1.win and not player2.win:
            displaysurf.blit(GameTexts[6], (GAMEWIDTH/2-30, GAMEHEIGHT/2-30))
        elif not player1.win:
            # If player 1 lost, player 2 wins
            displaysurf.blit(GameTexts[7], (GAMEWIDTH/2-150, GAMEHEIGHT/2-15))
        elif not player2.win:
            # If player 2 lost, player 1 wins
            displaysurf.blit(GameTexts[8], (GAMEWIDTH/2-150, GAMEHEIGHT/2-15))

        # Draw Starting Counter, match starts at mapTime 0, but "GO" stays in screen until 1s
        if Timers[1] < 60:
            if 0 < Timers[0] < 60:
                displaysurf.blit(GameTexts[2], (600, 450))
            elif 60 < Timers[0] < 120:
                displaysurf.blit(GameTexts[3], (600, 450))
            elif 120 < Timers[0] < 180:
                displaysurf.blit(GameTexts[4], (600, 450))
            if Timers[0] > 180:
                displaysurf.blit(GameTexts[5], (570, 430))

        # Draw Pause Surface if match has Started and game is paused, draw the Pause Surface.
        if GamePause and Timers[1] > 1:
            PauseSurface.blit(displaysurf, (0, 0))

            PauseSurface.blit(ButtonIcons[9], (30, 800))
            PauseSurface.blit(ButtonIcons[10], (160, 800))
            PauseSurface.blit(ButtonIcons[11], (290, 800))
            PauseSurface.blit(ButtonIcons[12], (430, 800))
            PauseSurface.blit(ButtonIcons[13], (550, 835))

            PauseSurface.blit(ButtonIcons[0], (130, 815))
            PauseSurface.blit(ButtonIcons[0], (250, 815))
            PauseSurface.blit(ButtonIcons[0], (385, 815))
            if getJoys > 0:
                PauseSurface.blit(ButtonIcons[1], (30, 700))
                PauseSurface.blit(ButtonIcons[2], (160, 700))
                PauseSurface.blit(ButtonIcons[4], (290, 700))
                PauseSurface.blit(ButtonIcons[3], (420, 700))

                PauseSurface.blit(ButtonIcons[0], (130, 715))
                PauseSurface.blit(ButtonIcons[0], (250, 715))
                PauseSurface.blit(ButtonIcons[0], (380, 715))

                PauseSurface.blit(ButtonIcons[5], (30, 600))
                PauseSurface.blit(ButtonIcons[6], (160, 600))
                PauseSurface.blit(ButtonIcons[8], (290, 600))
                PauseSurface.blit(ButtonIcons[7], (420, 600))

                PauseSurface.blit(ButtonIcons[0], (130, 615))
                PauseSurface.blit(ButtonIcons[0], (250, 615))
                PauseSurface.blit(ButtonIcons[0], (380, 615))

            PauseSurface.blit(GameTexts[1], (GAMEWIDTH/2-100, GAMEHEIGHT/2-50))
            displaysurf.blit(PauseSurface, (0, 0))

        # Display mouse crosshair last
        if getJoys < 2:
            displaysurf.blit(gameCursor, cursorRect)

        # If Different Resolution, draw everything to scaled window.
        if windowresize:
            frame = pygame.transform.scale(displaysurf, (windowx, windowy))
            window.blit(frame, frame.get_rect())

        pygame.display.update()  # Updates the player's screen with everything we've just drawn.

    # when run= False
    pygame.quit()


# Runs the game if this is main run module
if __name__ == '__main__':
    main()
