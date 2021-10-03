from math import atan,radians,degrees
from random import randint


MAPHEIGHT =896
GAMEWIDTH=1280
GAMEHEIGHT=964
    
def randomChipTimes():
    '''Generates 6 random times going upwards in a list'''
    returnList = []
    for i in range(12):
        a = randint(i*900,i*900+900)
        if i==1 or i==3 or i==5 or i==7 or i==9 or i==11:
            maybe = randint(0,1)
            if maybe: a = -1 #Never to load, so maybe it doesn't spawn a lot of chips
        returnList.append(a)
    return returnList
    
def angletoState(angle): 
    if 0 <= angle <= 22.5 or angle >= 337.5: state = ('R',0)
    elif 22.5 <= angle <= 67.5: state = ('R','U')
    elif 67.5 <= angle <= 90: state = ('R','U',False)
    elif 90 <= angle <= 112.5: state = ('L','U',False)
    elif 112.5 <= angle <= 157.5: state = ('L','U')
    elif 157.5 <= angle <= 202.5: state = ('L',0)
    elif 202.5 <= angle <= 252.5: state = ('L','D')
    elif 252.5 <= angle <= 270: state = ('L','D',False)
    elif 270 <= angle <= 292.5: state = ('R','D',False)
    elif 292.5 <= angle <= 337.5: state = ('R','D')
    return state

def pointToAngle(p1,p2,tooCloseCancel=True):
    x1,y1 = p1
    x2,y2 = p2
    distx = x2-x1
    disty = y2-y1
    if tooCloseCancel:
        PointDist = (distx**2 + disty**2)**0.5
        if PointDist < 40: tooClose = True
        else: tooClose = False
        if tooClose: return None
    #Avoid div by 0
    if distx == 0:
        if disty > 0: PointAngle = 90
        elif disty < 0: PointAngle = 270
        if disty == 0: PointAngle = 0
        return PointAngle
    
    PointAngle = atan(disty/distx)
    PointAngle = abs(degrees(PointAngle))
    
    if distx>0 and disty > 0: pass
    elif distx < 0 and disty > 0: PointAngle = 180- PointAngle
    elif distx < 0 and disty < 0: PointAngle += 180
    elif distx > 0 and disty < 0: PointAngle = 360- PointAngle

    if disty == 0:
        if distx < 0: PointAngle = 180
        elif distx > 0: PointAngle = 0
    
    return PointAngle
    

    
def stickto360(stickx,sticky):
    stickx *= 100
    sticky *= -100 #Y axis is inverted so fix that
    PointDist = (stickx**2 + sticky**2)**0.5
    if PointDist < 25: Deadzoned = True
    else: Deadzoned = False
    if Deadzoned: return None
    #Avoid div by /0
    if stickx == 0:
        if sticky > 0: PointAngle = 90
        elif sticky < 0: PointAngle = 270
        elif sticky == 0: PointAngle = 0
        state = angletoState(PointAngle)
        return (PointAngle)

    
    PointAngle = atan(sticky/stickx)
    PointAngle = abs(degrees(PointAngle))
    if stickx>0 and sticky > 0: pass
    elif stickx < 0 and sticky > 0: PointAngle = 180- PointAngle
    elif stickx < 0 and sticky < 0: PointAngle += 180
    elif stickx > 0 and sticky < 0: PointAngle = 360- PointAngle
    return (PointAngle)

#Line Implementations
def pointdist(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    squared = (x2-x1)**2+(y2-y1)**2
    return squared**0.5

def solveQuadratic(a,b,c):
    sol = -b + (b**2-4*a*c)**0.5
    sol /= 2*a
    sol2 = -b - (b**2-4*a*c)**0.5
    sol2 /= 2*a
    return (sol,sol2)

def getNegslope(p1,p2):
    x1,y1 = p1
    x2,y2 = p2

    slope = (y2-y1)/(x2-x1)
    negslope = -1/slope

    return negslope
def midpoint(p1,p2):
    x1,y1 = p1
    x2,y2 = p2

    return ((x2+x1)/2,(y2+y1)/2)

def getB(p1,slope):
    #gets slope and point, returns cut with y
    x,y = p1
    b = y-slope*x
    return b

def getSidePoints(p1,p2,Pcheck,threshold):
    slope = getNegslope(p1,p2)
    b = getB(Pcheck,slope)   
    d = threshold
    p,q = Pcheck
    z = b-q
    x1,x2 = solveQuadratic((1+slope**2),(-2*p+2*z*slope),(p**2+z**2-d**2))
    y1 = slope*x1+b
    y2 = slope*x2+b
    return ((x1,y1),(x2,y2))

def splitpoints(p1,p2,splits):
    '''Receives two points and a split, returns points that split p1 and p2 in splits segments'''
    x1,y1 = p1
    x2,y2 = p2
    pointlist = []
    splitter = 1 #current point
    for repeater in range(splits-1): #there are splits-1 points, there are 3 segments are splitted by 2 points.
        pointlist.append( ( x1-( (x1-x2)/splits*splitter),y1-( (y1-y2)/splits*splitter)    )     )
        splitter +=1
        
    return pointlist

def getStraightSidePoints(p1,threshold,vertical):
    x,y = p1
    if vertical:
        return ((x+threshold,y),(x-threshold,y))
    else:
        return ((x,y+threshold),(x,y-threshold))

def generatePoints(point1,point2):
    x1,y1 = point1
    x2,y2 = point2
    threshold = randint(-15,15)
    splitter = randint(3,9)
    if pointdist(point1,point2)> 600: splitter = randint(8,12)
    if pointdist(point1,point2)> 1000: splitter = randint(14,22)
    splitlist = splitpoints(point1,point2,splitter)
    if x2-x1 != 0 and y2-y1 != 0:
        pointlist = [point1]
        for point in splitlist:
            pointlist.extend( getSidePoints(point1,point2,point,threshold) )
        pointlist.append(point2)
    elif x2-x1 == 0:
        pointlist = [point1]
        for point in splitlist:
            pointlist.extend(getStraightSidePoints(point,threshold,True))
        pointlist.append(point2)
    elif y2-y1 == 0:
        pointlist = [point1]
        for point in splitlist:
            pointlist.extend(getStraightSidePoints(point,threshold,False))
        pointlist.append(point2)

    for x,y in pointlist:
        print (pointlist)
        if not isinstance(x,(float,int)):
            print (x)
            raise ValueError('Complex number received')
    return pointlist

#Rect/Line Collision Implementation

def orientation(p,q,r):
    '''receives 3 set of points and returns orientation,
    0 --> collinear
    1 --> clockwise
    -1 --> counterclockwise'''
    px,py = p
    qx,qy = q
    rx,ry = r
    orientation = (qy-py)*(rx-qx)-(qx-px)*(ry-qy)

    if orientation == 0: return 0
    if (orientation > 0): return 1
    else: return -1

def onSegment(p,q,r):
    '''GIVEN p,q,r collinear then checks if point q lies on segment pr'''
    px,py = p
    qx,qy = q
    rx,ry = r

    if (qx <= max(px,rx) and qx >= min(px,rx) and qy <= max(py,ry) and
        qy >= min(py,ry)): return True

    return False

def intersect(p1,q1,p2,q2):
    ''' Check if two segments p1-q1 and p2-q2 intersect'''
    o1 = orientation(p1,q1,p2)
    o2 = orientation(p1,q1,q2)
    o3 = orientation(p2,q2,p1)
    o4 = orientation(p2,q2,q1)

    if (o1 != o2 and o3 != o4):
        return True

    #Special cases
    if (o1 == 0 and onSegment(p1,p2,q1)): return True
    if (o2 == 0 and onSegment(p1,q2,q1)): return True

    if (o3 == 0 and onSegment(p2,p1,q2)): return True
    if (o4 == 0 and onSegment(p2,q1,q2)): return True

    return False

def fixY(p):
    '''Receives a point, and returns another point with inversed Y according to set GAMEHEIGHT'''
    x,y = p
    return (x,GAMEHEIGHT-y)
def rectlinecollide(rect,p1,p2):
    '''Receives a pygame.rect object and p1 and p2, checks if rect collides
    with segment p1-p2 '''
    p1 = fixY(p1)
    p2 = fixY(p2)
    topleft = (rect.left,rect.top)
    topleft = fixY(topleft)
    topright = (rect.right,rect.top)
    topright = fixY(topright)
    
    bottomleft = (rect.left,rect.bottom)
    bottomleft = fixY(bottomleft)
    bottomright = (rect.right,rect.bottom)
    bottomright = fixY(bottomright)
    topPoints = splitpoints(topleft,topright,10)
    bottomPoints = splitpoints(bottomleft,bottomright,10)

    lineList = []
    for index in range(9): #there are 9 splitpoints 
        lineList.append( (topPoints[index],bottomPoints[index]) ) #creates a list of segments
        
    lineList.insert(0, (topleft,bottomleft) ) #insert rect left and right sides to the list
    lineList.append( (topright,bottomright) )
    
    for segment in lineList:
        p,q = segment
        if intersect(p,q,p1,p2):
            return True
        
    return False
    


