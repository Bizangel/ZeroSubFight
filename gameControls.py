import pygame
from collections import namedtuple
import Modules.extraFunctions as extra
Move = namedtuple('move',['up','left','right'])
#Y axis follows inverted screen pattern -1 when up 1 when fully down
joyMapXbox = { 'A' : 0,
               'B' : 1,
               'X' : 2,
               'Y' : 3,
               'LB': 4,
               'RB': 5,
               'Select': 6,
               'Start': 7,
               'LS': 8,
               'RS':9,
               'LeftStickX': 0,
               'LeftStickY': 1,
               'Triggers': 2, #LT positive, RT negative
               'RightStickY':3,
               'RightStickX':4
               }
joyMapPs4 = { 'Square' : 0,
              'X' : 1,
              'Circle': 2,
              'Triangle': 3,
              'L1':4,
              'R1':5,
              'L2':6, #Hair Triggers
              'R2':7, #Hair Triggers
              'Share':8,
              'Options':9,
              'LS' : 10,
              'RS' : 11,
              'PsButton' : 12,
              'Touchpad' : 13,
              'LeftStickX': 0,
              'LeftStickY': 1,
              'RightStickX': 2,
              'RightStickY': 3,
              'LeftTrigger': 5,
              'RightTrigger' :4
              }
def GameControls(player,bulletasset,joystick=None):
    '''Receives player and joystick, if no joystick uses keyboard controls, updates player status and actions according to the hardware'''
    #resets values and changes after updating.
    player.remotetrigger = False
    moveleft = False
    moveright = False
    moveup = False
    player.didShoot = False
    #Game Controls #If xbox in pygame.joystick.get_name()
    #Gets Axis and buttons as list  
    if joystick != None: #if joystick exists
        buttons = []
        axis = []
        layout1 = False
        if 'xbox' in (joystick.get_name()).lower() or 'xinput' in (joystick.get_name()).lower(): nButtons,nAxis,layout1 = 10,5,True
        else:nButtons,nAxis = 14,6
        for i in range(nButtons):
            a = joystick.get_button(i)
            buttons.append(a)
        for i in range(nAxis):
            a = joystick.get_axis(i)
            axis.append(a)
        if layout1:
            if axis[joyMapXbox['LeftStickX']] < -0.5: moveleft= True
            if axis[joyMapXbox['LeftStickX']] > 0.5: moveright = True
            if axis[joyMapXbox['Triggers']] < -0.5: player.Shoot(bulletasset)
            if buttons[joyMapXbox['B']]: player.nadethrow()
            if buttons[joyMapXbox['A']]: moveup = True
            player.move = Move(moveup,moveleft,moveright)
            #Sets Y direction
            if axis[joyMapXbox['LeftStickY']] < -0.5: player.Yfacing = 'U'
            elif axis[joyMapXbox['LeftStickY']] > 0.5 : player.Yfacing = 'D'
            else: player.Yfacing = 0
            
            player.setAngle( extra.stickto360(axis[joyMapXbox['RightStickX']],axis[joyMapXbox['RightStickY']]) )
            if player.angle == None:
                player.state = None
                player.shootAngle = None
            else:
                player.state = extra.angletoState(player.angle)
            player.stateUpdate()
            player.optBulxvel,player.optBulyvel = player.weaponAdjust()
            if player.angle != None:
                player.shootAngle = player.angle
        else:
            if axis[joyMapPs4['LeftStickX']] < -0.5: moveleft = True
            if axis[joyMapPs4['LeftStickX']] > 0.5: moveright = True
            if axis[joyMapPs4['RightTrigger']] > 0.5: player.Shoot(bulletasset)
            if buttons[joyMapPs4['X']]: moveup = True
            if buttons[joyMapPs4['Circle']]: player.nadethrow()
            player.move = Move(moveup,moveleft,moveright)
            #Sets Y direction
            if axis[joyMapPs4['LeftStickY']] < -0.5: player.Yfacing = 'U'
            elif axis[joyMapPs4['LeftStickY']] > 0.5 : player.Yfacing = 'D'
            else: player.Yfacing = 0

            player.setAngle( extra.stickto360(axis[joyMapPs4['RightStickX']],axis[joyMapPs4['RightStickY']]) )
            
            if player.angle == None:
                player.state = None
                player.shootAngle = None
            else:
                player.state = extra.angletoState(player.angle)
            player.stateUpdate()
            player.optBulxvel,player.optBulyvel = player.weaponAdjust()
            if player.angle != None:
                player.shootAngle = player.angle
            
        
    #Keyboard controls
    #Player 1 if only 1 or no controlers
    elif joystick == None and player.stringname == 'player1':
        keys = pygame.key.get_pressed()
        player.move = Move(keys[pygame.K_SPACE],keys[pygame.K_a],keys[pygame.K_d])
        if keys[pygame.K_x]: player.Shoot(bulletasset)
        if keys[pygame.K_r] or keys[pygame.K_q]: player.nadethrow()
        if keys[pygame.K_w]: player.Yfacing = 'U'
        if pygame.mouse.get_pressed()[0]:player.Shoot(bulletasset)
        elif keys[pygame.K_s]: player.Yfacing = 'D'
        else: player.Yfacing = 0
    #Player 2 on keyboard
    elif joystick == None and player.stringname == 'player2':
        keys = pygame.key.get_pressed()
        player.move = Move(keys[pygame.K_c],keys[pygame.K_j],keys[pygame.K_l])
        if keys[pygame.K_v]: player.Shoot(bulletasset)
        if keys[pygame.K_t]: player.nadethrow()
        if keys[pygame.K_i]: player.Yfacing ='U'
        elif keys[pygame.K_k]: player.Yfacing = 'D'
        else: player.Yfacing = 0
def PauseControls(canPause,player,GamePause,menuBreak,joystick=None):

    if joystick != None:
        buttons = []
        axis = []
        layout1 = False
        
        if 'xbox' in (joystick.get_name()).lower() or 'xinput' in (joystick.get_name()).lower(): nButtons,nAxis,layout1 = 10,5,True
        else:nButtons,nAxis = 14,6
        for i in range(nButtons):
            a = joystick.get_button(i)
            buttons.append(a)
        for i in range(nAxis):
            a = joystick.get_axis(i)
            axis.append(a)
            
        if layout1:
            if buttons[joyMapXbox['A']] and buttons[joyMapXbox['LB']] and buttons[joyMapXbox['RB']] and buttons[joyMapXbox['X']] and GamePause:
                menuBreak = True
            if buttons[joyMapXbox['Start']]: player.trypause(canPause)
        else:
            if buttons[joyMapPs4['X']] and buttons[joyMapPs4['Square']] and buttons[joyMapPs4['L1']] and buttons[joyMapPs4['R1']] and GamePause:
                menuBreak = True
            if buttons[joyMapPs4['Options']]:player.trypause(canPause)
    else:
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and keys[pygame.K_w] and keys[pygame.K_e] and keys[pygame.K_SPACE]and GamePause:
            menuBreak = True
        #print (keys[pygame.K_z], keys[pygame.K_x] , keys[pygame.K_SPACE], GamePause)
        if keys[pygame.K_ESCAPE]: player.trypause(canPause)



    return menuBreak
            

    
def MenuControls(MenuPos,MenuInfo,SoundEffects,joystick=None):
    onMenu = True #if this is getting read so yeah
    MenuPlay,MenuSettings,MusicVolume,SFXVolume,run,MenuActionDone,Mute,spedup,MenuCoords,Endless,runMap,gameGo = MenuInfo
    click,menuclick,menuswitch = SoundEffects[0],SoundEffects[1],SoundEffects[2]
    moveleft = False
    moveright = False
    moveup = False
    movedown = False
    confirm = False
    goback = False
    #Gets all joystick and keyboard inputs, and then does calculations
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_DOWN]: movedown = True
    if keys[pygame.K_UP]: moveup = True
    if keys[pygame.K_LEFT]: moveleft = True
    if keys[pygame.K_RIGHT]: moveright = True
    if keys[pygame.K_RETURN] or keys[pygame.K_z]: confirm = True
    if keys[pygame.K_ESCAPE]: goback = True
    
    if joystick != None: 
        buttons = []
        axis = []
        layout1 = False
        if 'xbox' in (joystick.get_name()).lower() or 'xinput' in (joystick.get_name()).lower(): nButtons,nAxis,layout1 = 10,5,True
        else:nButtons,nAxis = 14,6
        for i in range(nButtons):
            a = joystick.get_button(i)
            buttons.append(a)
        for i in range(nAxis):
            a = joystick.get_axis(i)
            axis.append(a)
        if layout1:
            if buttons[joyMapXbox['A']]: confirm = True
            if buttons[joyMapXbox['B']]: goback = True
            if axis[joyMapXbox['LeftStickX']] < -0.5: moveleft= True
            if axis[joyMapXbox['LeftStickX']] > 0.5: moveright = True
            if axis[joyMapXbox['LeftStickY']] < -0.5: moveup = True
            if axis[joyMapXbox['LeftStickY']] > 0.5: movedown = True
            dpad = joystick.get_hat(0) #tuple, follows normal (X,Y) (0,1) means up for example
            if dpad[0] == 1: moveright = True
            if dpad[0] == -1: moveleft = True
            if dpad[1] == 1: moveup = True
            if dpad[1] == -1: movedown = True
        else:
            #ps4
            if buttons[joyMapPs4['X']]: confirm = True
            if buttons[joyMapPs4['Circle']]: goback = True
            if axis[joyMapPs4['LeftStickX']] < -0.5: moveleft= True
            if axis[joyMapPs4['LeftStickX']] > 0.5: moveright = True
            if axis[joyMapPs4['LeftStickY']] < -0.5: moveup = True
            if axis[joyMapPs4['LeftStickY']] > 0.5: movedown = True
            dpad = joystick.get_hat(0) 
            if dpad[0] == 1: moveright = True
            if dpad[0] == -1: moveleft = True
            if dpad[1] == 1: moveup = True
            if dpad[1] == -1: movedown = True
            
    #Do Menu Sounds
    if not MenuPlay and not MenuSettings: #Main menu
        if MenuPos < 2 and movedown:
            menuclick.stop()
            menuclick.play()
        if MenuPos > 0 and moveup:
            menuclick.stop()
            menuclick.play()
    elif MenuSettings:
        if MenuPos < 3 and movedown:
            menuclick.stop()
            menuclick.play()
        if MenuPos > 0 and moveup:
            menuclick.stop()
            menuclick.play()
        
    if MenuPos == -1 and (movedown or moveup):
        MenuPos = 0

    elif movedown:
        MenuPos +=1
        if MenuPos > 2 and not MenuPlay and not MenuSettings: MenuPos = 2
        elif MenuPos > 3 and MenuSettings: MenuPos = 3
        elif MenuPlay: MenuPos = -1
        

    elif moveup:
        MenuPos -=1
        if MenuPos < 0: MenuPos = 0
    #Actions
    if not MenuPlay and not MenuSettings:
        if confirm:
            if MenuPos == 0: MenuPlay = True
            elif MenuPos == 1: MenuSettings,MenuPos = True,-1
            elif MenuPos == 2: run = False #exit game option
            menuswitch.play()
    elif MenuSettings:
        if goback:
            MenuSettings,MenuPos = False,1
            menuswitch.play()
        elif confirm and MenuPos == 3:
            MenuSettings,MenuPos = False,-1
            menuswitch.play()
        else:
            if confirm and MenuPos == 2:
                if Mute: Mute = False
                else: Mute = True
                menuswitch.play()
            if moveleft and MenuPos == 0:
                if spedup: MusicVolume -=5
                else: MusicVolume -=1
                if MusicVolume <0: MusicVolume = 0
                click.stop()
                click.play()
            elif moveright and MenuPos == 0:
                if spedup: MusicVolume +=5
                else: MusicVolume +=1
                if MusicVolume >100: MusicVolume = 100
                click.stop()
                click.play()

            if moveleft and MenuPos == 1:
                if spedup: SFXVolume -=5
                else: SFXVolume -=1
                if SFXVolume < 0: SFXVolume = 0
                click.stop()
                click.play()
            
            elif moveright and MenuPos == 1:
                if spedup: SFXVolume +=5
                else: SFXVolume += 1    
                if SFXVolume > 100: SFXVolume = 100
                click.stop()
                click.play()
    elif MenuPlay:
        #do sounds
        if moveleft and MenuCoords[0] == 1 and MenuCoords[1] != 3:
            menuclick.stop()
            menuclick.play()
        if moveright and MenuCoords[0] == 0 and MenuCoords[1] != 3:
            menuclick.stop()
            menuclick.play()
        if moveup and MenuCoords[1] > 0:
            menuclick.stop()
            menuclick.play()
        if movedown and MenuCoords[1] < 3:
            menuclick.stop()
            menuclick.play()
        if confirm:
            menuclick.stop()
            menuswitch.play()
        if goback:
            MenuPlay,MenuPos = False,0
            menuswitch.play()
        else:
            if confirm and MenuCoords == [1,0]:
                if Endless: Endless = False
                else: Endless = True

            elif confirm and MenuCoords == [0,0]:  runMap = 0
            elif confirm and MenuCoords == [0,1]:  runMap = 1
            elif confirm and MenuCoords == [1,1]:  runMap = 2
            elif confirm and MenuCoords == [0,2]:  runMap = 3
            elif confirm and MenuCoords == [1,2]:  runMap = 4
            if (MenuCoords == [0,3] or MenuCoords == [1,3]) and confirm:
                onMenu = False
                gameGo = True
                    
            if moveleft:
                MenuCoords[0] -=1
                if MenuCoords[0] <0: MenuCoords[0] = 0
            elif moveright:
                MenuCoords[0] +=1
                if MenuCoords[0] >1: MenuCoords[0] = 1

            if moveup:
                MenuCoords[1] -=1
                if MenuCoords[1] < 0: MenuCoords[1] = 0
            elif movedown:
                MenuCoords[1] +=1
                if MenuCoords[1] > 3: MenuCoords[1] = 3
            
    
            
    
    if moveleft or moveright or moveup or movedown or confirm or goback: MenuActionDone = True
    if not MenuActionDone: spedup = False
    return MenuPos,MenuPlay,MenuSettings,MusicVolume,SFXVolume,run,MenuActionDone,Mute,spedup,onMenu,MenuCoords,Endless,runMap,gameGo
            
        
