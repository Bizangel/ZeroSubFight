import extraFunctions as extra

p1,p2 = (464, 327),(229, 423)


pointlist = extra.generatePoints(p1,p2)

for x,y in pointlist:
        if not isinstance(x,(float,int)):
            print (arg1,arg2)
            print (x)
            raise ValueError('Complex number received')
