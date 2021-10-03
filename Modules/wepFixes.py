def wepAdjust(wepID,bulx,buly,xface,yface,onGround,still,diagonal):
    ''' Receives a weapon ID, bulx and buly,player X and Y facing, and fixes bullet
    spawn x and y so it spawns properly and looks like it is coming out of the gun'''
    R = 'R'
    L = 'L'
    U = 'U'
    D = 'D'
    
    if wepID == 0 or wepID == 4:
        #Plasma adjustments
        if onGround:
            if still:
                if yface == 0 and xface == 'L': bulx += 0
                if yface == 0 and xface == 'R': bulx += -10
                elif diagonal:
                    
                    if xface == 'R':
                        if yface == 'U': bulx += 5
                        elif yface == 'D':
                           bulx += 8
                           buly -= 33
                    
                    elif xface == 'L':
                        if yface == 'U': bulx+= -5
                        elif yface == 'D':
                            bulx -= 5
                            buly -= 35

                else:
                    if yface == 'U':
                        if xface == 'R': bulx += -10
                        elif xface == 'L': bulx += 15
                    elif yface == 'D':
                        if xface == 'R': bulx += 15
                        elif xface == 'L': bulx += -10
                        
            elif xface == 'R':
                if yface == 0: buly += 0
                elif yface == 'U': bulx += 5
                elif yface == 'D':
                    bulx -= 5
                    buly -= 40
            elif xface == 'L':
                if yface == 0: buly += 0
                elif yface == 'U': bulx+= -5
                elif yface == 'D':
                    bulx -= 5
                    buly -= 35
        else:
            #Not on ground
            if yface == 0:
                if xface == 'R': bulx += 0
                elif xface == 'L': bulx += 0
            elif diagonal:
                if xface == 'L':
                    if yface == 0: buly +=0
                    elif yface == 'U': bulx += -5
                    elif yface == 'D':
                        bulx += -12
                        buly += -18
                elif xface == 'R':
                    if yface == 0: buly += 0
                    elif yface == 'U': bulx += 0
                    elif yface == 'D':
                        bulx += 10
                        buly += -15
            else:
                if yface == 'U':
                    if xface == 'R':bulx += -5
                    elif xface == 'L': bulx += 0
                elif yface == 'D':
                    if xface == 'R': bulx += 2
                    elif xface == 'L': bulx -= 10
            
    elif wepID == 1:
        #Laser adjustments
        if onGround:
            if still:
                if yface == 0 and xface == 'L':
                    bulx += -8
                    buly += 7
                if yface == 0 and xface == 'R':
                    bulx += 9
                    buly += 7
                elif diagonal:
                    
                    if xface == 'R':
                        if yface == 'U':
                            bulx += 24
                            buly += -5
                        elif yface == 'D':
                           bulx += 35
                           buly -= 7
                    
                    elif xface == 'L':
                        if yface == 'U':
                            bulx += 2
                            buly += -3
                        elif yface == 'D':
                            bulx -= 17
                            buly -= 6

                else:
                    if yface == 'U':
                        if xface == 'R':
                            bulx += -2
                            buly += -8
                        elif xface == 'L':
                            bulx += 20
                            buly += -5
                    elif yface == 'D':
                        if xface == 'R': bulx += 22
                        elif xface == 'L': bulx += -0
                        
            elif xface == 'R':
                if yface == 0:
                    bulx += 9
                    buly += 7
                elif yface == 'U':
                    bulx += 35
                    buly += -5
                elif yface == 'D':
                    bulx += 35
                    buly -= 7
            elif xface == 'L':
                if yface == 0:
                    bulx += -8
                    buly += 7
                elif yface == 'U':
                    bulx += -10
                    buly += -3
                elif yface == 'D':
                    bulx -= 17
                    buly -= 6
        else:
            #Not on ground
            if yface == 0:
                if xface == 'R':
                    bulx += 9
                    buly += 7
                elif xface == 'L':
                    bulx += -8
                    buly += 7
            
            elif diagonal:
                if xface == 'R':
                    if yface == 'U':
                        bulx += 24
                        buly += -5
                    elif yface == 'D':
                       bulx += 35
                       buly -= 7
                
                elif xface == 'L':
                    if yface == 'U':
                        bulx += -12
                        buly += -4
                    elif yface == 'D':
                        bulx -= 17
                        buly -= 6
            else:
                if yface == 'U':
                    if xface == 'R':
                        bulx += 0
                        buly += -8
                    elif xface == 'L':
                        bulx += 6
                        buly += -5
                elif yface == 'D':
                    if xface == 'R':
                        bulx += 10
                        buly += 10
                    elif xface == 'L': bulx += 0
                    
    elif wepID == 2:
        if onGround:
            if still:
                if yface == 0 and xface == 'L': bulx += -20
                if yface == 0 and xface == 'R': bulx += 0
                elif diagonal:
                    
                    if xface == 'R':
                        if yface == 'U':
                            bulx += 10
                            buly -= 10
                        elif yface == 'D':
                           bulx += 15
                           buly -= 23
                    
                    elif xface == 'L':
                        if yface == 'U':
                            bulx+= -10
                            buly -= 10
                        elif yface == 'D':
                            bulx -= 20
                            buly -= 23

                else:
                    if yface == 'U':
                        if xface == 'R':
                            buly -= 10
                            bulx += -15
                        elif xface == 'L':
                            buly -= 10
                            bulx += 10
                    elif yface == 'D':
                        if xface == 'R': bulx += 5
                        elif xface == 'L': bulx += -15
                        
            elif xface == 'R':
                if yface == 0: bulx += 3
                elif yface == 'U':
                    bulx += 10
                    buly -= 10 
                elif yface == 'D':
                    bulx += 10
                    buly -= 20
            elif xface == 'L':
                if yface == 0: bulx += -5
                elif yface == 'U':
                    bulx += -10
                    buly -=5
                elif yface == 'D':
                    bulx -= 10
                    buly -= 20
        else:
            #Not on ground
            if yface == 0:
                if xface == 'R': bulx += 5
                elif xface == 'L': bulx += -20
            elif diagonal:
                if xface == 'R':
                    if yface == 'U':
                        bulx += 10
                        buly -= 10
                    elif yface == 'D':
                       bulx += 15
                       buly -= 10
                    
                elif xface == 'L':
                    if yface == 'U':
                        bulx += -20
                        buly -= 15
                    elif yface == 'D':
                        bulx -= 30
                        buly -= 20

                    
            else:
                if yface == 'U':
                    if xface == 'R':
                        bulx += -15
                        buly -= 5
                    elif xface == 'L':
                        bulx += -10
                        buly -=5
                elif yface == 'D':
                    if xface == 'R': bulx += -5
                    elif xface == 'L': bulx -= 20
                    
    elif wepID == 3:
        if onGround:
            if still:
                if yface == 0 and xface == 'L':
                    bulx += -15
                    buly -= 15
                if yface == 0 and xface == 'R':
                    bulx += 0
                    buly -= 15
                elif diagonal:
                    
                    if xface == 'R':
                        if yface == 'U':
                            bulx += 10
                            buly -= 23
                        elif yface == 'D':
                           bulx += 20
                           buly -= 30
                    
                    elif xface == 'L':
                        if yface == 'U':
                            bulx+= -10
                            buly -= 25
                        elif yface == 'D':
                            bulx -= 20
                            buly -= 28

                else:
                    if yface == 'U':
                        if xface == 'R':
                            buly -= 10
                            bulx += -20
                        elif xface == 'L':
                            buly -= 10
                            bulx += -5
                    elif yface == 'D':
                        if xface == 'R': bulx += 0
                        elif xface == 'L': bulx += -25
                        
            elif xface == 'R':
                if yface == 0:
                    bulx += 0
                    buly -= 15
                elif yface == 'U':
                    bulx += 10
                    buly -= 23
                elif yface == 'D':
                    bulx += 20
                    buly -= 30
            elif xface == 'L':
                if yface == 0:
                    bulx += -15
                    buly -= 15
                elif yface == 'U':
                    bulx+= -10
                    buly -= 25
                elif yface == 'D':
                    bulx -= 20
                    buly -= 28
        else:
            #Not on ground
            if yface == 0:
                if xface == 'R':
                    bulx += 0
                    buly -= 15
                elif xface == 'L':
                    bulx += -15
                    buly -= 15
            elif diagonal:
                if xface == 'R':
                    if yface == 'U':
                        bulx += 10
                        buly -= 30
                    elif yface == 'D':
                       bulx += 15
                       buly -= 30
                    
                elif xface == 'L':
                    if yface == 'U':
                        bulx += -20
                        buly -= 15
                    elif yface == 'D':
                        bulx -= 25
                        buly -= 30

                    
            else:
                if yface == 'U':
                    if xface == 'R':
                        buly -= 10
                        bulx += -15
                    elif xface == 'L':
                        buly -= 10
                        bulx += -5
                elif yface == 'D':
                    if xface == 'R': bulx += 0
                    elif xface == 'L': bulx += -25
                
            
            
        
            


    return (bulx,buly)
    
