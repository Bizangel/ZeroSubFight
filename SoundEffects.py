import pygame
def LoadSFX():
    '''Loads all game sounds'''
    click = pygame.mixer.Sound('Sounds/SFX/click.ogg')
    menuclick = pygame.mixer.Sound('Sounds/SFX/menuclick.ogg')
    menuswitch = pygame.mixer.Sound('Sounds/SFX/menuswitch.ogg')

    chipPickUp = pygame.mixer.Sound('Sounds/SFX/chipPickUp.ogg') #3
    chipSpawn = pygame.mixer.Sound('Sounds/SFX/chipSpawn.ogg') #4
    grenade = pygame.mixer.Sound('Sounds/SFX/grenade.ogg') #5
    teleport = pygame.mixer.Sound('Sounds/SFX/teleport.ogg') #6
    explosion = pygame.mixer.Sound('Sounds/SFX/explosion.ogg') #7
    
    
    returnList =[click,menuclick,menuswitch, chipPickUp, chipSpawn,grenade,teleport,explosion]
    return returnList
