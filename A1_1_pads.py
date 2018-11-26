from numpy import *
from jason_functions import *
from pf import pf

#Set spaces relevant to traces.
d2 = pf['trace_space']

#Define array with pixel centers, numbered by order of trace, where 1 is lowest (most left) and 7 is highest (most right).
#Naming convention is quandrant_sector_pixeltracenumber.
length1 = 13
#length2 = 14
#length3 = 16

A1_1_left_pos = [2502. + i*pf['xpitch'] for i in range(length1)]
A1_1_left_neg = [2647. + i*pf['xpitch'] for i in range(length1)]
#A1_2_left_pos = [-1792.5 + i*pf['xpitch'] for i in range(length2)]
#A1_2_left_neg = [-1647.5 + i*pf['xpitch'] for i in range(length2)]
#A1_3_left_pos = [2267.5 + i*pf['xpitch'] for i in range(length3)]
#A1_3_left_neg = [2412.5 + i*pf['xpitch'] for i in range(length3)]

turnpoint = 4400.
angle = -60.
notrace = -1.

extra_left = -6750.
name = 'pad_A_1_1'

top = [-30., 475., 1752.704 - 0.6 + 100. - 2.*3.46 + 2.*178.17 + 100.]
############################################################################################################################
#################################Don't touch this....#######################################################################
trace = open(r'/Users/jathaniminium/xic/sptpol6_traces/traces/'+name+'.txt', 'w')
trace.write('(Traces for ' + name + ');\n')

locations = []
check = 0.
for i in range(length1):
	left = A1_1_left_neg[i] - 6.84 - 5.159
	A1_1 = [0.,top[0]]
	#Bring traces up from bond pads to appropriate space above pads.
	A1_1[0],A1_1[1] = A1_1[0] + left , A1_1[1] - 25.
	limit = top[1] - 25.
	diff = abs(A1_1[1] - limit)
	trace.write('(SymbolCall A1_trace_W11_50);\n')
	while (A1_1[1] < limit):
		if (diff > 50.):
			A1_1[1] += 49.
		else:
			A1_1[1] += diff
		diff = abs(A1_1[1] - limit)
		trace.write('9 A1_trace_W11_50;\n')
		x, y= rotate(A1_1[0], A1_1[1], angle)
		trace.write('C 0 T ' + str(int(1000.*x)) + ' ' + str(int(1000.*y)) + ';\n')
	trace.write('(SymbolCall A1_trace_W21_52);\n')
	trace.write('9 A1_trace_W21_52;\n')
	x,y = rotate(A1_1[0], A1_1[1] - 1., angle)
	trace.write('C 0 T ' + str(int(1000.*x)) + ' ' + str(int(1000.*y)) + ';\n')

	#Tack on a converter piece to give the W11 trace more room next to the bond pad.
	#A1_1[1] += 20.
	#trace.write('(SymbolCall A1_trace_pad_step);\n')
	#trace.write('9 A1_trace_pad_step;\n')
	#x,y = rotate(A1_1[0], A1_1[1] - 1., angle)
	#trace.write('C 0 T ' + str(int(1000.*x)) + ' ' + str(int(1000.*y)) + ';\n')

		#Bring up to the appropriate height above the negative pad for nesting traces.
	#First, see which side of the turnpoint you land on.
	turn_location = turnpoint
	delta = left - turnpoint
	npads = delta/pf['xpitch']
	
	count = abs(round(npads))
	
	limit = top[1] + (count-1.)*50. - 25.
	diff = abs(A1_1[1] - limit)
	trace.write('(SymbolCall A1_trace_straight_W11_W21_50);\n')
	while(A1_1[1] < limit):
		if (diff > 50.):
			A1_1[1] += 49.
		else:
			A1_1[1] += diff
		diff = abs(A1_1[1] - limit)
		trace.write('9 A1_trace_straight_W11_W21_50;\n')
		x,y = rotate(A1_1[0], A1_1[1], angle)
		trace.write('C 0 T ' + str(int(1000.*x)) + ' ' + str(int(1000.*y)) + ';\n')

	A1_1[1] += 49.
	if npads < 0. and abs(npads) > 0.5:
		trace.write('(SymbolCall A1_trace_straight_W11_W21_left_corner_down);\n')
		trace.write('9 A1_trace_straight_W11_W21_left_corner_down;\n')
		x,y = rotate(A1_1[0], A1_1[1], angle)
		trace.write('C 0 T ' + str(int(1000.*x)) + ' ' + str(int(1000.*y)) + ';\n')

	if npads > 0. and abs(npads) > 0.5:
		trace.write('(SymbolCall A1_trace_straight_W21_W11_right_corner_down);\n')
		trace.write('9 A1_trace_straight_W21_W11_right_corner_down;\n')
		x,y = rotate(A1_1[0], A1_1[1], angle)
		trace.write('C 0 T ' + str(int(1000.*x)) + ' ' + str(int(1000.*y)) + ';\n')

	if abs(A1_1[0] - turn_location) < 145.:
		print 'Whoa!  Too close to the turn point!'
		use_me = A1_1[0]
		check = 1.

	locations.append([A1_1[0],A1_1[1]])
if check == 1.: turn_location = use_me
print 'Turn location = ', turn_location

locations2 = []
#Bring traces over to the turn location and bend up.
for i in range(length1):
	A1_1[0], A1_1[1] = locations[i][0] - 1., locations[i][1]
	
	left = A1_1_left_neg[i] - 3.
	delta = left - turnpoint
	npads = delta/pf['xpitch']
	count = abs(round(npads)) - 1.

	#if (A1_1[0] + 1.) == turn_location:
	if abs(A1_1[0] - turn_location) < 145.:
		A1_1[0] += 1.
		A1_1[1] -= 24.
		trace.write('(SymbolCall A1_trace_straight_W11_W21_50);\n')
		trace.write('9 A1_trace_straight_W11_W21_50;\n')
		x,y = rotate(A1_1[0], A1_1[1], angle)
		trace.write('C 0 T ' + str(int(1000.*x)) + ' ' + str(int(1000.*y)) + ';\n')

	elif (A1_1[0] + 1.) < turn_location:
	
		limit = turn_location - 88. - 50.*count
		diff = abs(A1_1[0] - turn_location)
		trace.write('(SymbolCall A1_trace_straight_W11_W21_H_50);\n')
		while (A1_1[0] < limit):
			if diff > 50.:
				A1_1[0] += 49.
			else:
				A1_1[0] += diff
			diff = abs(A1_1[0] - limit)
			trace.write('9 A1_trace_straight_W11_W21_H_50;\n')
			x,y = rotate(A1_1[0], A1_1[1], angle)
			trace.write('C 0 T ' + str(int(1000.*x)) + ' ' + str(int(1000.*y)) + ';\n')
		A1_1[0] += 38.
		#A1_1[0] += 10.
		trace.write('(SymbolCall A1_trace_straight_W11_W21_right_corner_up);\n')
		trace.write('9 A1_trace_straight_W11_W21_right_corner_up;\n')
		x,y = rotate(A1_1[0], A1_1[1], angle)
		trace.write('C 0 T ' + str(int(1000.*x)) + ' ' + str(int(1000.*y)) + ';\n')

	elif (A1_1[0] + 1.) > turn_location:
		A1_1[0] += 2.
		limit = turn_location + 88. + 50.*count
		diff = abs(A1_1[0] - turn_location)
		trace.write('(SymbolCall A1_trace_straight_W21_W11_H_50);\n')
		while (A1_1[0] > limit):
			if diff > 50.:
				A1_1[0] -= 49.
			else:
				A1_1[0] -= diff
			diff = abs(A1_1[0] - limit)
			trace.write('9 A1_trace_straight_W21_W11_H_50;\n')
			x,y = rotate(A1_1[0], A1_1[1], angle)
			trace.write('C 0 T ' + str(int(1000.*x)) + ' ' + str(int(1000.*y)) + ';\n')
		A1_1[0] -= 38.
		#A1_1[0] -= 10.
		trace.write('(SymbolCall A1_trace_straight_W21_W11_left_corner_up);\n')
		trace.write('9 A1_trace_straight_W21_W11_left_corner_up;\n')
		x,y = rotate(A1_1[0], A1_1[1], angle)
		trace.write('C 0 T ' + str(int(1000.*x)) + ' ' + str(int(1000.*y)) + ';\n')

	locations2.append([A1_1[0],A1_1[1]])

	#Bring all the traces up to appropriate location.
	if i > notrace:
		A1_1[1] -= 1.
		use = top[2]
		if i < 6.:
			use += 26.7925*(6.-i) 

		#use -= 0.12*i
			
		limit = use - 50. - (count - 1.)*13.398
		if i > 6: limit -= 2.*13.398
		diff = abs(A1_1[1] - limit)
		trace.write('(SymbolCall A1_trace_straight_W11_W21_25);\n')
		while(A1_1[1] < limit):
			if (diff > 25.):
				A1_1[1] += 24.
			else:
				A1_1[1] += diff
			diff = abs(A1_1[1] - limit)
			trace.write('9 A1_trace_straight_W11_W21_25;\n')
			x,y = rotate(A1_1[0], A1_1[1], angle)
			trace.write('C 0 T ' + str(int(1000.*x)) + ' ' + str(int(1000.*y)) + ';\n')

		#Tack on a 60 degree rotation piece to connect to the traces coming from the array.
		if i > notrace:
			A1_1[1] += 10.5
			trace.write('(SymbolCall A1_trace_W11_W21_30_left_down);\n')
			trace.write('9 A1_trace_W11_W21_30_left_down;\n')
			x,y = rotate(A1_1[0], A1_1[1], angle)
			trace.write('C 0 T ' + str(int(1000.*x)) + ' ' + str(int(1000.*y)) + ';\n')

trace.close()








