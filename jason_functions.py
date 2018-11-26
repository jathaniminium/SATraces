from numpy import *

#Rotate a vector about the z-axis.
def rotate(x,y,angle,xcent=0.,ycent=0.):
	x1 = x - xcent
	y1 = y - ycent

	#print 'x= ', x1
	#print 'y= ', y1

	x2 = (x1)*cos(angle*pi/180.) - (y1)*sin(angle*pi/180.) 
	y2 = (x1)*sin(angle*pi/180.) + (y1)*cos(angle*pi/180.)

	#print 'x2= ', x2
	#print 'y2= ', y2

	x2 += xcent
	y2 += ycent
	
	return x2, y2




#Calculate the distance between two points.
def distance(x1,y1,x2,y2):
	dx = x2 - x1
	dy = y2 - y1

	dist = sqrt(dx**2. + dy**2.)

	return dist
	
