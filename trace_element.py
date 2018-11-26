#from pf import *
from numpy import *
from jason_functions import *
import string

class trace_element:
	#Initiate common attributes used by all trace components. "pf" is a parameter file that contains all relevant information.
	def __init__(self, pf):
		# Amount each trace element overlaps with next and previous.
		self.overlap = pf["overlap"]
		# Center-center space between trace pairs.
		self.trace_space = pf["trace_space"]
		self.edge_buffer = pf["edge_buffer"]
		self.twist = pf['twist']
		self.twistlengthA = pf['twistlengthA']
		self.twistlengthB = pf['twistlengthB']
		self.bundle_high = pf['bundle_high']
		self.side = pf['side']

############################################################################################################################
############################################################################################################################
	#Take traces up.
	def u(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space

		#Does the next trace turn to the right?
		count = string.count(next_trace, 'ur')
		count2 = string.count(next_trace, '45')
		if count2 ==1:
			print 'count2:', count2
			space = 19.1342

		#Define the limits for trace growing.
		limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
		limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.)

		cell = 'trace_straight_W21_W11_ud'
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][1] -= self.overlap
			pos[1][1] -= self.overlap
			
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'left':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
				
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] < limit):
				if (diff > 95.):
					pos[0][1] += 95.
				else:
					pos[0][1] += diff
				diff = abs(pos[0][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'left':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] < limit):
				if (diff > 95.):
					pos[1][1] += 95.
				else:
					pos[1][1] += diff
				diff = abs(pos[1][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][1] += 100.
			pos[1][1] += 100.
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][1] -= self.overlap
			pos[1][1] -= self.overlap
			
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'left':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] < limit):
				if (diff > 95.):
					pos[0][1] += 95.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][1] += diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][1] -= 40.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][1] -= 40.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						cell = 'trace_straight_W11_W21_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W21_W11_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][1] - limit)
		

			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'left':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] < limit):
				if (diff > 95.):
					pos[1][1] += 95.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][1] += diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][1] -= 40.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][1] -= 40.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W11_W21_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W21_W11_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][1] - limit)
				
			pos[0][1] += 100.
			pos[1][1] += 100.
			lengthA += 100.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 100.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
				
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces up.
	def d(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space

		#Does the next trace turn to the left?
		count = string.count(next_trace, 'dl')
		count2 = string.count(next_trace, '45')
		if count2 ==1:
			print 'count2:', count2
			space = 19.1342

		#Define the limits for trace growing.
		limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
		limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 

		cell = 'trace_straight_W11_W21_ud'
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][1] += self.overlap
			pos[1][1] += self.overlap
			
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
				
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 95.):
					pos[0][1] -= 95.
				else:
					pos[0][1] -= diff
				diff = abs(pos[0][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 95.):
					pos[1][1] -= 95.
				else:
					pos[1][1] -= diff
				diff = abs(pos[1][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][1] -= 100.
			pos[1][1] -= 100.
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][1] += self.overlap
			pos[1][1] += self.overlap
			
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 95.):
					pos[0][1] -= 95.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][1] -= diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][1] += 40.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][1] += 40.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						cell = 'trace_straight_W21_W11_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][1] - limit)
		

			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 95.):
					pos[1][1] -= 95.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][1] -= diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][1] += 40.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][1] += 40.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W21_W11_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][1] - limit)
				
			pos[0][1] -= 100.
			pos[1][1] -= 100.
			lengthA += 100.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 100.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
				
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces down short.
	def d_short(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space

		#Does the next trace turn to the left?
		count = string.count(next_trace, 'dl')
		count2 = string.count(next_trace, '45')
		if count2 ==1:
			print 'count2:', count2
			space = 19.1342

		#Define the limits for trace growing.
		limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
		limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 

		cell = 'trace_straight_W11_W21_ud_short2'
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][1] -= self.overlap*2.
			pos[1][1] -= self.overlap*2.
			
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
				
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 20.):
					pos[0][1] -= 20.
				else:
					pos[0][1] -= diff
				diff = abs(pos[0][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 20.):
					pos[1][1] -= 20.
				else:
					pos[1][1] -= diff
				diff = abs(pos[1][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][1] -= 50.
			pos[1][1] -= 50.
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][1] += self.overlap
			pos[1][1] += self.overlap
			
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 20.):
					pos[0][1] -= 20.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][1] -= diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][1] += 40.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][1] += 40.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						cell = 'trace_straight_W21_W11_ud_short2'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_ud_short2'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][1] - limit)
		

			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) 
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.) 
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 20.):
					pos[1][1] -= 20.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][1] -= diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][1] += 40.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][1] += 40.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W21_W11_ud_short2'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_ud_short2'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][1] - limit)
				
			pos[0][1] -= 50.
			pos[1][1] -= 50.
			lengthA += 50.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 50.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
				
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces left.
	def l(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Does the next trace turn down?
		count = string.count(next_trace, 'ld')
		count2 = string.count(next_trace, '45')
		if count2 ==1:
			print 'count2:', count2
			space = 19.1342

		#Define the limits for trace growing.
		limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
		limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.)

		cell = 'trace_straight_W11_W21_lr'
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][0] += self.overlap
			pos[1][0] += self.overlap
			wires.write('(SymbolCall ' + cell +');\n')
			
			if count == 1:  #We ARE turning DOWN.
				print 'Turning DOWN.'
				limit2 = edge + self.edge_buffer + space*(2.*(self.bundle_high - bundle_num -1.) + 1.)
				limit1 = edge + self.edge_buffer + space*2.*(self.bundle_high - bundle_num -1.)
				limit = limit1
			else: #We are turning UP.
				limit = limit2
			diff = abs(pos[0][0] - limit)
			while (pos[0][0] > limit):
				if (diff > 95.):
					pos[0][0] -= 95.
				else:
					pos[0][0] -= diff
				diff = abs(pos[0][0] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			wires.write('(SymbolCall ' + cell +');\n')
			if count == 1:  #We ARE turning DOWN.
				limit2 = edge + self.edge_buffer + space*(2.*(self.bundle_high - bundle_num -1.) + 1.)
				limit1 = edge + self.edge_buffer + space*2.*(self.bundle_high - bundle_num -1.)
				limit = limit2
			else: #We are turning UP.
				limit = limit1
			diff = abs(pos[1][0] - limit)
			while (pos[1][0] > limit):
				if (diff > 95.):
					pos[1][0] -= 95.
				else:
					pos[1][0] -= diff
				diff = abs(pos[1][0] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] -= 100.
			pos[1][0] -= 100.
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][0] += self.overlap
			pos[1][0] += self.overlap
			if count == 1:  #We ARE turning DOWN.
				limit2 = edge + self.edge_buffer + space*(2.*(self.bundle_high - bundle_num -1.) + 1.)
				limit1 = edge + self.edge_buffer + space*2.*(self.bundle_high - bundle_num -1.)
				limit = limit1
			else: #We are turning UP.
				limit = limit2
			diff = abs(pos[0][0] - limit)
			while (pos[0][0] > limit):
				if (diff > 95.):
					pos[0][0] -= 95.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][0] -= diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][0] += 40.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W11_W21_25_H;\n')
					else:
						wires.write('9 trace_cross_W21_W11_25_H;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][0] += 40.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						cell = 'trace_straight_W21_W11_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][0] - limit)
		

			if count == 1:  #We ARE turning DOWN.
				limit2 = edge + self.edge_buffer + space*(2.*(self.bundle_high - bundle_num -1.) + 1.)
				limit1 = edge + self.edge_buffer + space*2.*(self.bundle_high - bundle_num -1.)
				limit = limit2
			else: #We are turning UP.
				limit = limit1
			diff = abs(pos[1][0] - limit)
			while (pos[1][0] > limit):
				if (diff > 95.):
					pos[1][0] -= 95.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][0] -= diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][0] += 40.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W11_W21_25_H;\n')
					else:
						wires.write('9 trace_cross_W21_W11_25_H;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][0] += 40.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W21_W11_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][0] - limit)

			pos[0][0] -= 100.
			pos[1][0] -= 100.
			lengthA += 100.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 100.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################

############################################################################################################################
############################################################################################################################
	#Take traces right.
	def r(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space

		cell = 'trace_straight_W21_W11_lr'

		#Does the next trace turn up?
		count = string.count(next_trace, 'rd')
		count2 = string.count(next_trace, '45')
		if count2 ==1:
			print 'count2:', count2
			space = 19.1342

		#Define the limits for trace growing.
		limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
		limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][0] -= self.overlap
			pos[1][0] -= self.overlap
			wires.write('(SymbolCall ' + cell +');\n')
			
			if count == 1:  #We ARE turning DOWN.
				limit = limit2
			else: #We are turning UP.
				limit1 = edge + self.edge_buffer + space*(2.*(self.bundle_high - bundle_num -1.) + 1.)
				limit2 = edge + self.edge_buffer + space*2.*(self.bundle_high - bundle_num -1.)
				limit = limit1
			print 'limit: ', limit
			diff = abs(pos[0][0] - limit)
			while (pos[0][0] < limit):
				if (diff > 95.):
					pos[0][0] += 95.
				else:
					pos[0][0] += diff
				diff = abs(pos[0][0] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			wires.write('(SymbolCall ' + cell +');\n')
			if count == 1:  #We ARE turning DOWN.
				limit = limit1
			else: #We are turning UP.
				limit1 = edge + self.edge_buffer + space*(2.*(self.bundle_high - bundle_num -1.) + 1.)
				limit2 = edge + self.edge_buffer + space*2.*(self.bundle_high - bundle_num -1.)
				limit = limit2
			print 'limit: ', limit
			diff = abs(pos[1][0] - limit)
			while (pos[1][0] < limit):
				if (diff > 95.):
					pos[1][0] += 95.
				else:
					pos[1][0] += diff
				diff = abs(pos[1][0] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] += 100.
			pos[1][0] += 100.
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][0] -= self.overlap
			pos[1][0] -= self.overlap
			
			if count == 1:  #We ARE turning DOWN.
				limit = limit2
			else: #We are turning UP.
				limit1 = edge + self.edge_buffer + space*(2.*(self.bundle_high - bundle_num -1.) + 1.)
				limit2 = edge + self.edge_buffer + space*2.*(self.bundle_high - bundle_num -1.)
				limit = limit1
			diff = abs(pos[0][0] - limit)
			while (pos[0][0] < limit):
				if (diff > 95.):
					pos[0][0] += 95.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][0] += diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.:
					pos[0][0] -= 40.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.:
						wires.write('9 trace_cross_W11_W21_25_H;\n')
					else:
						wires.write('9 trace_cross_W21_W11_25_H;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][0] -= 40.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.:
						cell = 'trace_straight_W11_W21_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W21_W11_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][0] - limit)
		

			if count == 1:  #We ARE turning DOWN.
				limit = limit1
			else: #We are turning UP.
				limit1 = edge + self.edge_buffer + space*(2.*(self.bundle_high - bundle_num -1.) + 1.)
				limit2 = edge + self.edge_buffer + space*2.*(self.bundle_high - bundle_num -1.)
				limit = limit2
			diff = abs(pos[1][0] - limit)
			while (pos[1][0] < limit):
				if (diff > 95.):
					pos[1][0] += 95.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][0] += diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.:
					pos[1][0] -= 40.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.:
						wires.write('9 trace_cross_W11_W21_25_H;\n')
					else:
						wires.write('9 trace_cross_W21_W11_25_H;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][0] -= 40.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.:				
						cell = 'trace_straight_W11_W21_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W21_W11_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][0] - limit)

			pos[0][0] += 100.
			pos[1][0] += 100.
			lengthA += 100.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 100.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
				
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################

############################################################################################################################
############################################################################################################################
	#Turn the corner:up to the right.
	def ur(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 52.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 52.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W11_W21_ur'
			else:
				cell = 'trace_straight_W21_W11_ur'

			pos[0][1] -= self.overlap + 24.
			pos[1][1] -= self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W11_W21_ur'
			else:
				cell = 'trace_straight_W21_W11_ur'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] -= 19.
			pos[1][0] -= 19.
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W21_W11_ur'
			pos[0][1] -= self.overlap + 24.
			pos[1][1] -= self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] -= 19.
			pos[1][0] -= 19.
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################

############################################################################################################################
############################################################################################################################
	#Turn the corner:right to the up.
	def ru(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 52.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 52.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W11_W21_ru'
			else:
				cell = 'trace_straight_W21_W11_ru'

			pos[0][0] -= self.overlap + 24.
			pos[1][0] -= self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W11_W21_ru'
			else:
				cell = 'trace_straight_W21_W11_ru'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][1] -= 19.
			pos[1][1] -= 19.
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W21_W11_ru'
			pos[0][0] -= self.overlap + 24.
			pos[1][0] -= self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][1] -= 19.
			pos[1][1] -= 19.
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################

############################################################################################################################
############################################################################################################################
	#Turn the corner:up to the left.
	def ul(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 52.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 52.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W21_W11_ul'
			else:
				cell = 'trace_straight_W11_W21_ul'

			pos[0][1] -= self.overlap + 24.
			pos[1][1] -= self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W21_W11_ul'
			else:
				cell = 'trace_straight_W11_W21_ul'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] += 19.
			pos[1][0] += 19.
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W11_W21_ul'
			pos[0][1] -= self.overlap + 24.
			pos[1][1] -= self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] += 19.
			pos[1][0] += 19.
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################

############################################################################################################################
############################################################################################################################
	#Turn the corner:left to the up.
	def lu(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 52.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 52.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W11_W21_lu'
			else:
				cell = 'trace_straight_W21_W11_lu'

			pos[0][0] += self.overlap + 24.
			pos[1][0] += self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W11_W21_lu'
			else:
				cell = 'trace_straight_W21_W11_lu'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][1] -= 19.
			pos[1][1] -= 19.
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W21_W11_lu'
			pos[0][0] += self.overlap + 24.
			pos[1][0] += self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][1] -= 19.
			pos[1][1] -= 19.
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################

############################################################################################################################
############################################################################################################################
	#Turn the corner:left to the down.
	def ld(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 52.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 52.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W21_W11_ld'
			else:
				cell = 'trace_straight_W11_W21_ld'

			pos[0][0] += self.overlap + 24.
			pos[1][0] += self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W21_W11_ld'
			else:
				cell = 'trace_straight_W11_W21_ld'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][1] += 19.
			pos[1][1] += 19.
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W11_W21_ld'
			pos[0][0] += self.overlap + 24.
			pos[1][0] += self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][1] += 19.
			pos[1][1] += 19.
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################

############################################################################################################################
############################################################################################################################
	#Turn the corner:right to the down.
	def rd(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 52.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 52.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W11_W21_rd'
			else:
				cell = 'trace_straight_W21_W11_rd'

			pos[0][0] -= self.overlap + 24.
			pos[1][0] -= self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W11_W21_rd'
			else:
				cell = 'trace_straight_W21_W11_rd'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][1] += 19.
			pos[1][1] += 19.
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W21_W11_rd'
			pos[0][0] -= self.overlap + 24.
			pos[1][0] -= self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][1] += 19.
			pos[1][1] += 19.
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################

############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the right.
	def dr(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 52.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 52.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W21_W11_dr'
			else:
				cell = 'trace_straight_W11_W21_dr'

			pos[0][1] += self.overlap + 24.
			pos[1][1] += self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W21_W11_dr'
			else:
				cell = 'trace_straight_W11_W21_dr'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] -= 19.
			pos[1][0] -= 19.
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W11_W21_dr'
			pos[0][1] += self.overlap + 24.
			pos[1][1] += self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] -= 19.
			pos[1][0] -= 19.
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################

############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def dl(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 52.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 52.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W21_W11_dl'
			else:
				cell = 'trace_straight_W11_W21_dl'

			pos[0][1] += self.overlap + 24.
			pos[1][1] += self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W21_W11_dl'
			else:
				cell = 'trace_straight_W11_W21_dl'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] += 19.
			pos[1][0] += 19.
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W11_W21_dl'
			pos[0][1] += self.overlap + 24.
			pos[1][1] += self.overlap + 24.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] += 19.
			pos[1][0] += 19.
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces up to the right at a 45 degree angle.
	def ur45(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space

		#Does the next trace turn to the right?
		count = string.count(next_trace, 'ur45u')
		if count ==1:
			space = 19.1342

		#Define the limits for trace growing.
		limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) - 82.53
		limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.) - 82.53

		cell = 'trace_straight_W21_W11_ur45'
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][0] -= 5.*self.overlap
			pos[1][0] -= 5.*self.overlap
			pos[0][1] -= 5.*self.overlap
			pos[1][1] -= 5.*self.overlap
			
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = edge + self.edge_buffer - space*(2.*(self.bundle_high - bundle_num -1.) + 1.) - 82.53
			else: #We are turning RIGHT.
				limit = limit1
				
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] < limit):
				if (diff > 70.71):
					pos[0][0] += 65.
					pos[0][1] += 65.
				else:
					pos[0][0] += diff
					pos[0][1] += diff
				diff = abs(pos[0][1] - limit)
				wires.write('9 ' + cell + ';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = edge + self.edge_buffer - space*2.*(self.bundle_high - bundle_num -1.) - 82.53
			else: #We are turning RIGHT.
				limit = limit2
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] < limit):
				if (diff > 70.71):
					pos[1][0] += 65.
					pos[1][1] += 65.
				else:
					pos[1][0] += diff
					pos[1][1] += diff
				diff = abs(pos[1][1] - limit)
				wires.write('9 ' + cell + ';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] += 70.71
			pos[0][1] += 70.71
			pos[1][0] += 70.71
			pos[1][1] += 70.71
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][0] -= 5.*self.overlap
			pos[0][1] -= 5.*self.overlap
			pos[1][0] -= 5.*self.overlap
			pos[1][1] -= 5.*self.overlap
			
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = edge + self.edge_buffer - space*(2.*(self.bundle_high - bundle_num -1.) + 1.) - 82.53
			else: #We are turning RIGHT.
				limit = limit1
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] < limit):
				if (diff > 70.71):
					pos[0][0] += 65.
					pos[0][1] += 65.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][0] += diff
					pos[0][1] += diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][0] -= 21.
					pos[0][1] -= 21.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25_m45;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25_m45;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][0] -= 21.
					pos[0][1] -= 21.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						cell = 'trace_straight_W11_W21_ur45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W21_W11_ur45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][1] - limit)
		

			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = edge + self.edge_buffer - space*2.*(self.bundle_high - bundle_num -1.) - 82.53
			else: #We are turning RIGHT.
				limit = limit2
				
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] < limit):
				if (diff > 70.71):
					pos[1][0] += 65.
					pos[1][1] += 65.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][0] += diff
					pos[1][1] += diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][0] -= 21.
					pos[1][1] -= 21.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25_m45;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25_m45;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][0] -= 21.
					pos[1][1] -= 21.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W11_W21_ur45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W21_W11_ur45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][1] - limit)
				
			pos[0][0] += 70.71
			pos[0][1] += 70.71
			pos[1][0] += 70.71
			pos[1][1] += 70.71
			lengthA += 70.71
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 70.71
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
				
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces up to the right at a 45 degree angle.
	def dl45(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space

		#Does the next trace turn to the left?
		count = string.count(next_trace, 'dl45d')
		if count ==1:
			space = 19.1342

		#Define the limits for trace growing.
		limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
		limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.)

		cell = 'trace_straight_W11_W21_dl45'
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][0] += 5.*self.overlap
			pos[1][0] += 5.*self.overlap
			pos[0][1] += 5.*self.overlap
			pos[1][1] += 5.*self.overlap
			
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We are turning DOWN.
				limit = limit2
			else: #We are turning LEFT.
				limit = limit2
				
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 70.71):
					pos[0][0] -= 65.
					pos[0][1] -= 65.
				else:
					pos[0][0] -= diff
					pos[0][1] -= diff
				diff = abs(pos[0][1] - limit)
				wires.write('9 ' + cell + ';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = limit1
			else: #We are turning RIGHT.
				limit = limit1
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 70.71):
					pos[1][0] -= 65.
					pos[1][1] -= 65.
				else:
					pos[1][0] -= diff
					pos[1][1] -= diff
				diff = abs(pos[1][1] - limit)
				wires.write('9 ' + cell + ';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] -= 70.71
			pos[0][1] -= 70.71
			pos[1][0] -= 70.71
			pos[1][1] -= 70.71
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][0] += 5.*self.overlap
			pos[0][1] += 5.*self.overlap
			pos[1][0] += 5.*self.overlap
			pos[1][1] += 5.*self.overlap
			
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = limit2
			else: #We are turning RIGHT.
				limit = limit2
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 70.71):
					pos[0][0] -= 65.
					pos[0][1] -= 65.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][0] -= diff
					pos[0][1] -= diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][0] += 26.
					pos[0][1] += 26.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25_m45;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25_m45;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][0] += 26.
					pos[0][1] += 26.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						cell = 'trace_straight_W21_W11_dl45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_dl45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][1] - limit)
		

			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = limit1
			else: #We are turning RIGHT.
				limit = limit1
				
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 70.71):
					pos[1][0] -= 65.
					pos[1][1] -= 65.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][0] -= diff
					pos[1][1] -= diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][0] += 21.
					pos[1][1] += 21.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25_m45;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25_m45;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][0] += 21.
					pos[1][1] += 21.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W21_W11_dl45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_dl45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][1] - limit)
				
			pos[0][0] -= 70.71
			pos[0][1] -= 70.71
			pos[1][0] -= 70.71
			pos[1][1] -= 70.71
			lengthA += 70.71
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 70.71
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
				
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces up to the right at a 45 degree angle.
	def dr45(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space

		#Does the next trace turn to the right?
		count = string.count(next_trace, 'dr45r')
		if count ==0:
			print "We're turning down!"
			space = 19.1342

		#Define the limits for trace growing.
		limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
		limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.)

		cell = 'trace_straight_W11_W21_dr45'
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][0] -= 5.*self.overlap
			pos[0][1] += 5.*self.overlap
			pos[1][0] -= 5.*self.overlap
			pos[1][1] += 5.*self.overlap
			
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning RIGHT.
				limit = edge + self.edge_buffer
				limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
				limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
				limit = limit1
			else: #We are turning DOWN.
				limit = limit1
				
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 70.71):
					pos[0][0] += 65.
					pos[0][1] -= 65.
				else:
					pos[0][0] += diff
					pos[0][1] -= diff
				diff = abs(pos[0][1] - limit)
				wires.write('9 ' + cell + ';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = edge + self.edge_buffer
				limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
				limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
				limit = limit2
			else: #We are turning RIGHT.
				limit = limit2
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 70.71):
					pos[1][0] += 65.
					pos[1][1] -= 65.
				else:
					pos[1][0] += diff
					pos[1][1] -= diff
				diff = abs(pos[1][1] - limit)
				wires.write('9 ' + cell + ';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] += 70.71
			pos[0][1] -= 70.71
			pos[1][0] += 70.71
			pos[1][1] -= 70.71
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][0] -= 5.*self.overlap
			pos[0][1] += 5.*self.overlap
			pos[1][0] -= 5.*self.overlap
			pos[1][1] += 5.*self.overlap
			
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = edge + self.edge_buffer
				limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
				limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
				limit = limit1
			else: #We are turning RIGHT.
				limit = limit1
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 70.71):
					pos[0][0] += 65.
					pos[0][1] -= 65.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][0] += diff
					pos[0][1] -= diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][0] -= 21.
					pos[0][1] += 21.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25_45;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25_45;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][0] -= 21.
					pos[0][1] += 21.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						cell = 'trace_straight_W21_W11_dr45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_dr45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][1] - limit)
		

			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = edge + self.edge_buffer
				limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
				limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
				limit = limit2
			else: #We are turning RIGHT.
				limit = limit2
				
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 70.71):
					pos[1][0] += 65.
					pos[1][1] -= 65.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][0] += diff
					pos[1][1] -= diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][0] -= 21.
					pos[1][1] += 21.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25_45;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25_45;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][0] -= 21.
					pos[1][1] += 21.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W21_W11_dr45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_dr45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][1] - limit)
				
			pos[0][0] += 70.71
			pos[0][1] -= 70.71
			pos[1][0] += 70.71
			pos[1][1] -= 70.71
			lengthA += 70.71
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 70.71
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
				
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces up to the right at a 45 degree angle.
	def ul45(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space

		#Does the next trace turn to UP?
		count = string.count(next_trace, 'ul45u')
		if count ==1:
			space = 19.1342

		#Define the limits for trace growing.
		limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.) - 122.86
		limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.) - 122.86

		cell = 'trace_straight_W21_W11_ul45'
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][0] += 5.*self.overlap
			pos[0][1] -= 5.*self.overlap
			pos[1][0] += 5.*self.overlap
			pos[1][1] -= 5.*self.overlap
			
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = limit2
			else: #We are turning LEFT.
				limit = limit2
				
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] < limit):
				if (diff > 70.71):
					pos[0][0] -= 65.
					pos[0][1] += 65.
				else:
					pos[0][0] -= diff
					pos[0][1] += diff
				diff = abs(pos[0][1] - limit)
				wires.write('9 ' + cell + ';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = limit1
			else: #We are turning LEFT.
				limit = limit1
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] < limit):
				if (diff > 70.71):
					pos[1][0] -= 65.
					pos[1][1] += 65.
				else:
					pos[1][0] -= diff
					pos[1][1] += diff
				diff = abs(pos[1][1] - limit)
				wires.write('9 ' + cell + ';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] -= 70.71
			pos[0][1] += 70.71
			pos[1][0] -= 70.71
			pos[1][1] += 70.71
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][0] += 5.*self.overlap
			pos[0][1] -= 5.*self.overlap
			pos[1][0] += 5.*self.overlap
			pos[1][1] -= 5.*self.overlap
			
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = limit2
			else: #We are turning LEFT.
				limit = limit2
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] < limit):
				if (diff > 70.71):
					pos[0][0] -= 65.
					pos[0][1] += 65.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][0] -= diff
					pos[0][1] += diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][0] += 21.
					pos[0][1] -= 21.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25_45;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25_45;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][0] += 21.
					pos[0][1] -= 21.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						cell = 'trace_straight_W11_W21_ul45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W21_W11_ul45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][1] - limit)
		

			#Calcuate the trace limit based on edge and which way the trace is turning.
			if count == 1:  #We ARE turning Up.
				limit = limit1
			else: #We are turning LEFT.
				limit = limit1
				
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] < limit):
				if (diff > 70.71):
					pos[1][0] -= 65.
					pos[1][1] += 65.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][0] -= diff
					pos[1][1] += diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][0] += 21.
					pos[1][1] -= 21.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25_45;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25_45;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][0] += 21.
					pos[1][1] -= 21.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W11_W21_ul45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W21_W11_ul45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][1] - limit)
				
			pos[0][0] -= 70.71
			pos[0][1] += 70.71
			pos[1][0] -= 70.71
			pos[1][1] += 70.71
			lengthA += 70.71
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 70.71
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
				
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def ldl45(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W21_W11_ldl45'
			else:
				cell = 'trace_straight_W11_W21_ldl45'

			pos[0][0] += 3.*self.overlap
			pos[1][0] += 3.*self.overlap
			pos[0][1] -= 21.192
			pos[1][1] -= 21.192
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W21_W11_ldl45'
			else:
				cell = 'trace_straight_W11_W21_ldl45'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] += self.overlap
			pos[0][1] += self.overlap
			pos[1][0] += self.overlap
			pos[1][1] += self.overlap
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W11_W21_ldl45'
			pos[0][0] += 3.*self.overlap
			pos[1][0] += 3.*self.overlap
			pos[0][1] -= 21.192
			pos[1][1] -= 21.192
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] += self.overlap
			pos[0][1] += self.overlap
			pos[1][0] += self.overlap
			pos[1][1] += self.overlap
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def rdr45(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W21_W11_rdr45'
			else:
				cell = 'trace_straight_W11_W21_rdr45'

			pos[0][0] -= 55.
			pos[1][0] -= 55.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W21_W11_rdr45'
			else:
				cell = 'trace_straight_W11_W21_rdr45'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] += 29.97
			pos[1][0] += 29.97
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W11_W21_rdr45'
			pos[0][0] -= 55.
			pos[1][0] -= 55.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] += 29.97
			pos[1][0] += 29.97
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def rur45(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W11_W21_rur45'
			else:
				cell = 'trace_straight_W21_W11_rur45'

			pos[0][0] -= 70.711
			pos[1][0] -= 70.711
			pos[0][1] += 0.23
			pos[1][1] += 0.23
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W11_W21_rur45'
			else:
				cell = 'trace_straight_W21_W11_rur45'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] += 30.21
			pos[1][0] += 30.21
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W21_W11_rur45'
			pos[0][0] -= 70.711
			pos[1][0] -= 70.711
			pos[0][1] += 0.23
			pos[1][1] += 0.23
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			
			pos[0][0] += 30.21
			pos[1][0] += 30.21
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def ur45u(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W11_W21_ur45u'
			else:
				cell = 'trace_straight_W21_W11_ur45u'

			pos[0][0] -= 55.
			pos[1][0] -= 55.
			pos[0][1] -= 55.
			pos[1][1] -= 55.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W11_W21_ur45u'
			else:
				cell = 'trace_straight_W21_W11_ur45u'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] += 21.192
			pos[0][1] += self.overlap
			pos[1][0] += 21.192
			pos[1][1] += self.overlap
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W21_W11_ur45u'
			pos[0][0] -= 55.
			pos[1][0] -= 55.
			pos[0][1] -= 55.
			pos[1][1] -= 55.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] += 21.192
			pos[0][1] += self.overlap
			pos[1][0] += 21.192
			pos[1][1] += self.overlap
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def ur45r(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W11_W21_ur45r'
			else:
				cell = 'trace_straight_W21_W11_ur45r'

			#pos[0][0] -= 55.
			#pos[1][0] -= 55.
			pos[0][1] -= 30.21
			pos[1][1] -= 30.21
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W11_W21_ur45r'
			else:
				cell = 'trace_straight_W21_W11_ur45r'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] -= 54.
			pos[0][1] += 0.232
			pos[1][0] -= 54.
			pos[1][1] += 0.232
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W21_W11_ur45r'
			#pos[0][0] -= 55.
			#pos[1][0] -= 55.
			pos[0][1] -= 30.21
			pos[1][1] -= 30.21
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] -= 54.
			pos[0][1] += 0.232
			pos[1][0] -= 54.
			pos[1][1] += 0.232
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def dr45d(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W21_W11_dr45d'
			else:
				cell = 'trace_straight_W11_W21_dr45d'

			pos[0][0] += 40.
			pos[1][0] += 40.
			pos[0][1] -= 40.
			pos[1][1] -= 40.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W21_W11_dr45d'
			else:
				cell = 'trace_straight_W11_W21_dr45d'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] += 21.192
			pos[0][1] -= self.overlap
			pos[1][0] += 21.192
			pos[1][1] -= self.overlap
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W11_W21_dr45d'
			pos[0][0] -= 40.
			pos[1][0] -= 40.
			pos[0][1] += 40.
			pos[1][1] += 40.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] += 21.192
			pos[0][1] -= self.overlap
			pos[1][0] += 21.192
			pos[1][1] -= self.overlap
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def dr45r(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W21_W11_dr45r'
			else:
				cell = 'trace_straight_W11_W21_dr45r'

			pos[0][0] += 14.97
			pos[1][0] += 14.97
			pos[0][1] += 15.
			pos[1][1] += 15.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W21_W11_dr45r'
			else:
				cell = 'trace_straight_W11_W21_dr45r'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] -= 50.
			pos[1][0] -= 50.
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W11_W21_dr45r'
			pos[0][0] += 14.97
			pos[1][0] += 14.97
			pos[0][1] += 15.
			pos[1][1] += 15.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] -= 50.
			pos[1][0] -= 50.
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def ddr45(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W21_W11_ddr45'
			else:
				cell = 'trace_straight_W11_W21_ddr45'

			pos[0][1] += 55.
			pos[1][1] += 55.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W21_W11_ddr45'
			else:
				cell = 'trace_straight_W11_W21_ddr45'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][1] -= 29.97
			pos[1][1] -= 29.97
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W11_W21_ddr45'
			pos[0][1] += 55.
			pos[1][1] += 55.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][1] -= 29.97
			pos[1][1] -= 29.97
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def uur45(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W11_W21_uur45'
			else:
				cell = 'trace_straight_W21_W11_uur45'

			pos[0][1] -= 55.
			pos[1][1] -= 55.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W11_W21_uur45'
			else:
				cell = 'trace_straight_W21_W11_uur45'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][1] += 29.97
			pos[1][1] += 29.97
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W21_W11_uur45'
			pos[0][1] -= 55.
			pos[1][1] -= 55.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][1] += 29.97
			pos[1][1] += 29.97
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def lul45(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W11_W21_lul45'
			else:
				cell = 'trace_straight_W21_W11_lul45'

			pos[0][0] += 10.
			pos[1][0] += 10.
			pos[0][1] += 21.36
			pos[1][1] += 21.36
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W11_W21_lul45'
			else:
				cell = 'trace_straight_W21_W11_lul45'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] += 14.67
			pos[1][0] += 14.67
			pos[0][1] -= 15.
			pos[1][1] -= 15.
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W21_W11_lul45'
			pos[0][0] += 10.
			pos[1][0] += 10.
			pos[0][1] += 21.36
			pos[1][1] += 21.36
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			
			pos[0][0] += 14.67
			pos[1][0] += 14.67
			pos[0][1] -= 15.
			pos[1][1] -= 15.
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def ul45u(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W11_W21_ul45u'
			else:
				cell = 'trace_straight_W21_W11_ul45u'

			pos[0][0] += 29.97
			pos[1][0] += 29.97
#			pos[0][1] -= 55.
#			pos[1][1] -= 55.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W11_W21_ul45u'
			else:
				cell = 'trace_straight_W21_W11_ul45u'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

#			pos[0][0] -= 21.192
			pos[0][1] -= 45.
#			pos[1][0] -= 21.192
			pos[1][1] -= 45.
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W21_W11_ul45u'
			pos[0][0] += 29.97
			pos[1][0] += 29.97
#			pos[0][1] -= 55.
#			pos[1][1] -= 55.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
#			pos[0][0] -= 21.192
			pos[0][1] -= 45.
#			pos[1][0] -= 21.192
			pos[1][1] -= 45.
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def ul45l(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W11_W21_ul45l'
			else:
				cell = 'trace_straight_W21_W11_ul45l'

			pos[0][0] += 39.884
			pos[1][0] += 39.884
			pos[0][1] -= 40.21
			pos[1][1] -= 40.21
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W11_W21_ul45l'
			else:
				cell = 'trace_straight_W21_W11_ul45l'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

#			pos[0][0] -= 21.192
			pos[0][1] += 21.36
#			pos[1][0] -= 21.192
			pos[1][1] += 21.36
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W21_W11_ul45l'
			pos[0][0] += 39.884
			pos[1][0] += 39.884
			pos[0][1] -= 40.21
			pos[1][1] -= 40.21
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
#			pos[0][0] -= 21.192
			pos[0][1] += 21.36
#			pos[1][0] -= 21.192
			pos[1][1] += 21.36
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def dl45d(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W21_W11_dl45d'
			else:
				cell = 'trace_straight_W11_W21_dl45d	'

			pos[0][0] += 54.995
			pos[1][0] += 54.995
			pos[0][1] += 55.
			pos[1][1] += 55.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W21_W11_dl45d'
			else:
				cell = 'trace_straight_W11_W21_dl45d'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] -= 21.192
			pos[0][1] += 5.
			pos[1][0] -= 21.192
			pos[1][1] += 5.
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W11_W21_dl45d'
			pos[0][0] += 54.995
			pos[1][0] += 54.995
			pos[0][1] += 55.
			pos[1][1] += 55.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] -= 21.192
			pos[0][1] += 5.
			pos[1][0] -= 21.192
			pos[1][1] += 5.
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def ddl45(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W21_W11_ddl45'
			else:
				cell = 'trace_straight_W11_W21_ddl45'

			pos[0][0] -= 21.1915
			pos[1][0] -= 21.1915
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W21_W11_ddl45'
			else:
				cell = 'trace_straight_W11_W21_ddl45'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][0] += 10.
			pos[1][0] += 10.
			pos[0][1] += 10.
			pos[1][1] += 10.
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W11_W21_ddl45'
			pos[0][0] -= 21.1915
			pos[1][0] -= 21.1915
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] += 10.
			pos[1][0] += 10.
			pos[0][1] += 10.
			pos[1][1] += 10.
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def dl45l(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W21_W11_dl45l'
			else:
				cell = 'trace_straight_W11_W21_dl45l'

			pos[0][0] += 39.875
			pos[1][0] += 39.875
			pos[0][1] += 39.875
			pos[1][1] += 39.875
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W21_W11_dl45l'
			else:
				cell = 'trace_straight_W11_W21_dl45l'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

#			pos[0][0] -= 21.192
			pos[0][1] -= 21.1925
#			pos[1][0] -= 21.192
			pos[1][1] -= 21.1925
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W11_W21_dl45l'
			pos[0][0] += 39.875
			pos[1][0] += 39.875
			pos[0][1] += 39.875
			pos[1][1] += 39.875
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
#			pos[0][0] -= 21.192
			pos[0][1] -= 21.1925
#			pos[1][0] -= 21.192
			pos[1][1] -= 21.1925
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Turn the corner:down to the left.
	def uul45(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==1: # DO TWIST CALCULATIONS.

			lengthA += 59.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 59.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB

			#Which version of the trace element must we use?  This depends on how much the trace has rotated
			#since coming out of the pixel.
			if round(mod(twistA,2.)) > 0.:
				cell = 'trace_straight_W11_W21_uul45'
			else:
				cell = 'trace_straight_W21_W11_uul45'

			pos[0][1] -= 60.
			pos[1][1] -= 60.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			if round(mod(twistB,2.)) > 0.:
				cell = 'trace_straight_W11_W21_uul45'
			else:
				cell = 'trace_straight_W21_W11_uul45'
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')

			pos[0][1] += 29.97
			pos[1][1] += 29.97
			space = self.trace_space
			return pos, edge, twist_flags
			
		if self.twist==0:
			cell = 'trace_straight_W21_W11_uul45'
			pos[0][1] -= 60.
			pos[1][1] -= 60.
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
			wires.write('(SymbolCall ' + cell +');\n')
			wires.write('9 ' + cell + ';\n')
			wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][1] += 29.97
			pos[1][1] += 29.97
			space = self.trace_space
			return pos, edge
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces up to the right at a 45 degree angle.
	def dr45start(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = 19.1342

		#Define the limits for trace growing.
		limit2 = pos[0][1] - 75. #+ space*(2.*(bundle_num -1.) + 1.)
		limit1 = pos[1][1] - 75. #+ space*2.*(bundle_num -1.)

		cell = 'trace_straight_W11_W21_dr45'
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][0] -= 5.*self.overlap
			pos[0][1] += 5.*self.overlap
			pos[1][0] -= 5.*self.overlap
			pos[1][1] += 5.*self.overlap

#			pos[0][0] += 5.*self.overlap
#			pos[0][1] -= 5.*self.overlap
#			pos[1][0] += 5.*self.overlap
#			pos[1][1] -= 5.*self.overlap
			
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			#We are turning DOWN.

			if self.side == 'right':
				limit = limit2
			else:
				limit = limit2

			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 70.71):
					pos[0][0] += 65.
					pos[0][1] -= 65.
				else:
					pos[0][0] += diff
					pos[0][1] -= diff
				diff = abs(pos[0][1] - limit)
				wires.write('9 ' + cell + ';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				limit = limit1
			else:
				limit = limit1
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 70.71):
					pos[1][0] += 65.
					pos[1][1] -= 65.
				else:
					pos[1][0] += diff
					pos[1][1] -= diff
				diff = abs(pos[1][1] - limit)
				wires.write('9 ' + cell + ';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] += 70.71
			pos[0][1] -= 70.71
			pos[1][0] += 70.71
			pos[1][1] -= 70.71
#			pos[0][0] -= 5.
#			pos[0][1] += 5.
#			pos[1][0] -= 5.
#			pos[1][1] += 5.
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][0] -= 5.*self.overlap
			pos[0][1] += 5.*self.overlap
			pos[1][0] -= 5.*self.overlap
			pos[1][1] += 5.*self.overlap
			
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				limit = limit1
			else:
				limit = limit2
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 70.71):
					pos[0][0] += 65.
					pos[0][1] -= 65.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][0] += diff
					pos[0][1] -= diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][0] -= 21.
					pos[0][1] += 21.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25_45;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25_45;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][0] -= 21.
					pos[0][1] += 21.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						cell = 'trace_straight_W21_W11_dr45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_dr45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][1] - limit)
		

			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				limit = limit2
			else:
				limit = limit1
				
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 70.71):
					pos[1][0] += 65.
					pos[1][1] -= 65.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][0] += diff
					pos[1][1] -= diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][0] -= 21.
					pos[1][1] += 21.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25_45;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25_45;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][0] -= 21.
					pos[1][1] += 21.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W21_W11_dr45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_dr45'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][1] - limit)
				
			#pos[0][0] += 70.71
			#pos[0][1] -= 70.71
			#pos[1][0] += 70.71
			#pos[1][1] -= 70.71
			pos[0][0] -= 5.
			pos[0][1] += 5.
			pos[1][0] -= 5.
			pos[1][1] += 5.
			lengthA += 70.71
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 70.71
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
				
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces left.
	def l_end(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Define the limits for trace growing.
		limit = edge

		cell = 'trace_straight_W11_W21_lr_short'
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][0] -= 40.
			pos[1][0] -= 40.
			wires.write('(SymbolCall ' + cell +');\n')

			limit = edge + 13.5*2.*(7. - bundle_num)
			print 'limit=', limit
			diff = abs(pos[0][0] - limit)
			while (pos[0][0] > limit):
				if (diff > 45.):
					pos[0][0] -= 45.
				else:
					pos[0][0] -= diff
				diff = abs(pos[0][0] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			wires.write('(SymbolCall ' + cell +');\n')

			limit = edge + 13.5*2.*(7. - bundle_num) + 25.
			print 'limit=', limit
			diff = abs(pos[1][0] - limit)
			while (pos[1][0] > limit):
				if (diff > 45.):
					pos[1][0] -= 45.
				else:
					pos[1][0] -= diff
				diff = abs(pos[1][0] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] -= 50.
			pos[1][0] -= 50.
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][0] -= 7.*self.overlap
			pos[1][0] -= 7.*self.overlap

			limit = edge + 13.5*2.*(7. - bundle_num)
			diff = abs(pos[0][0] - limit)
			while (pos[0][0] > limit):
				if (diff > 45.):
					pos[0][0] -= 45.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][0] -= diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][0] += 40.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W11_W21_25_H;\n')
					else:
						wires.write('9 trace_cross_W21_W11_25_H;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][0] += 40.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						cell = 'trace_straight_W21_W11_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][0] - limit)

			limit = edge + 13.5*2.*(7. - bundle_num)
			diff = abs(pos[1][0] - limit)
			while (pos[1][0] > limit):
				if (diff > 45.):
					pos[1][0] -= 45.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][0] -= diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][0] += 40.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W11_W21_25_H;\n')
					else:
						wires.write('9 trace_cross_W21_W11_25_H;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][0] += 40.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W21_W11_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][0] - limit)

			pos[0][0] -= 50.
			pos[1][0] -= 50.
			lengthA += 50.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 50.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces right.
	def r_end(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space

		cell = 'trace_straight_W21_W11_lr'

		#Define the limits for trace growing.
		limit = edge
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][0] += 7.*self.overlap
			pos[1][0] += 7.*self.overlap
			wires.write('(SymbolCall ' + cell +');\n')

			limit = edge - 13.5*2.*(7. - bundle_num) #+ 25.
			diff = abs(pos[0][0] - limit)
			while (pos[0][0] < limit):
				if (diff > 45.):
					pos[0][0] += 45.
				else:
					pos[0][0] += diff
				diff = abs(pos[0][0] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			wires.write('(SymbolCall ' + cell +');\n')
			
			limit = edge - 13.5*(2.*(7. - bundle_num))
			diff = abs(pos[1][0] - limit)
			while (pos[1][0] < limit):
				if (diff > 45.):
					pos[1][0] += 45.
				else:
					pos[1][0] += diff
				diff = abs(pos[1][0] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] += 50.
			pos[1][0] += 50.
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][0] -= 7.*self.overlap
			pos[1][0] -= 7.*self.overlap
			
			limit = edge - 13.5*2.*(7. - bundle_num)
			diff = abs(pos[0][0] - limit)
			while (pos[0][0] < limit):
				if (diff > 45.):
					pos[0][0] += 45.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][0] += diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.:
					pos[0][0] -= 40.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.:
						wires.write('9 trace_cross_W11_W21_25_H;\n')
					else:
						wires.write('9 trace_cross_W21_W11_25_H;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][0] -= 40.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.:
						cell = 'trace_straight_W11_W21_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W21_W11_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][0] - limit)

			limit = edge - 13.5*(2.*(7. - bundle_num))
			diff = abs(pos[1][0] - limit)
			while (pos[1][0] < limit):
				if (diff > 45.):
					pos[1][0] += 45.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][0] += diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.:
					pos[1][0] -= 40.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.:
						wires.write('9 trace_cross_W11_W21_25_H;\n')
					else:
						wires.write('9 trace_cross_W21_W11_25_H;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][0] -= 40.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.:				
						cell = 'trace_straight_W11_W21_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W21_W11_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][0] - limit)

			pos[0][0] += 50.
			pos[1][0] += 50.
			lengthA += 50.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 50.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
				
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces up.
	def dstart(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space

		#Does the next trace turn to the left?
		count = string.count(next_trace, 'dl')
		count2 = string.count(next_trace, '45')
		if count2 ==1:
			print 'count2:', count2
			space = 19.1342

		#Define the limits for trace growing.
		limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
		limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.)



		cell = 'trace_straight_W11_W21_ud'
			
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][1] += self.overlap + 30.
			pos[1][1] += self.overlap + 30.

			if bundle_num == 7.:
				cell = 'trace_straight_W11_W21_ud'#_short2'
			#elif bundle_num == 6.:
			#	cell = 'trace_straight_W11_W21_ud_short'
			else:
				cell = 'trace_straight_W11_W21_ud'
			
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2

			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 95.):
					pos[0][1] -= 95.
				else:
					pos[0][1] -= diff
				diff = abs(pos[0][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')

			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 95.):
					pos[1][1] -= 95.
				else:
					pos[1][1] -= diff
				diff = abs(pos[1][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][1] -= 100.
			pos[1][1] -= 100.
			space = self.trace_space
			cell = 'trace_straight_W11_W21_ud'
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][1] += self.overlap + 30.
			pos[1][1] += self.overlap + 30.
			
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 95.):
					pos[0][1] -= 95.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][1] -= diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][1] += 40.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][1] += 40.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						if bundle_num == 7.:
							cell = 'trace_straight_W21_W11_ud_short2'
						elif bundle_num == 6.:
							cell = 'trace_straight_W21_W11_ud_short'
						else:
							cell = 'trace_straight_W21_W11_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						if bundle_num == 7.:
							cell = 'trace_straight_W21_W11_ud_short2'
						elif bundle_num == 6.:
							cell = 'trace_straight_W11_W21_ud_short'
						else:
							cell = 'trace_straight_W11_W21_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][1] - limit)
		

			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 95.):
					pos[1][1] -= 95.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][1] -= diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][1] += 40.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][1] += 40.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W21_W11_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][1] - limit)
				
			pos[0][1] -= 100.
			pos[1][1] -= 100.
			lengthA += 100.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 100.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
				
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces up.
	def dstart_short(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space

		#Does the next trace turn to the left?
		count = string.count(next_trace, 'dl')
		count2 = string.count(next_trace, '45')
		if count2 ==1:
			print 'count2:', count2
			space = 19.1342

		#Define the limits for trace growing.
		limit2 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
		limit1 = edge + self.edge_buffer + space*2.*(bundle_num -1.)



		cell = 'trace_straight_W11_W21_ud_short2'
			
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][1] += self.overlap
			pos[1][1] += self.overlap
			
			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2

			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 20.):
					pos[0][1] -= 20.
				else:
					pos[0][1] -= diff
				diff = abs(pos[0][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')

			wires.write('(SymbolCall ' + cell +');\n')
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 20.):
					pos[1][1] -= 20.
				else:
					pos[1][1] -= diff
				diff = abs(pos[1][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][1] -= 50.
			pos[1][1] -= 50.
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][1] += self.overlap
			pos[1][1] += self.overlap
			
			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 20.):
					pos[0][1] -= 20.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][1] -= diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][1] += 40.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][1] += 40.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						cell = 'trace_straight_W21_W11_ud_short2'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_ud_short2'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][1] - limit)
		

			#Calcuate the trace limit based on edge and which way the trace is turning.
			if self.side == 'right':
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit1
				else: #We are turning LEFT.
					limit = limit2
			else:
				if count == 1:  #We ARE turning Right.
					limit1 = edge + self.edge_buffer + space*(2.*(bundle_num -1.) + 1.)
					limit2 = edge + self.edge_buffer + space*2.*(bundle_num -1.)
					limit = limit2
				else: #We are turning LEFT.
					limit = limit1
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 20.):
					pos[1][1] -= 20.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][1] -= diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][1] += 40.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][1] += 40.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W21_W11_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][1] - limit)
				
			pos[0][1] -= 50.
			pos[1][1] -= 50.
			lengthA += 25.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 25.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
				
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces left.
	def u_end(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Define the limits for trace growing.
		limit = edge

		cell = 'trace_straight_W21_W11_ud'
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][1] -= 20.
			pos[1][1] -= 20.
			wires.write('(SymbolCall ' + cell +');\n')

			limit = edge
			print 'limit=', limit
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] < limit):
				if (diff > 95.):
					pos[0][1] += 95.
				else:
					pos[0][1] += diff
				diff = abs(pos[0][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			wires.write('(SymbolCall ' + cell +');\n')

			limit = edge
			print 'limit=', limit
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] < limit):
				if (diff > 95.):
					pos[1][1] += 95.
				else:
					pos[1][1] += diff
				diff = abs(pos[1][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] += 100.
			pos[1][0] += 100.
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][1] += 7.*self.overlap
			pos[1][1] += 7.*self.overlap

			limit = edge
			diff = abs(pos[0][0] - limit)
			while (pos[0][0] < limit):
				if (diff > 95.):
					pos[0][0] -= 95.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][1] += diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][1] -= 40.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W21_W11_25_ud;\n')
					else:
						wires.write('9 trace_cross_W11_W21_25_ud;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][1] -= 40.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						cell = 'trace_straight_W11_W21_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W21_W11_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][0] - limit)

			limit = edge
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] < limit):
				if (diff > 95.):
					pos[1][1] -= 95.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][1] += diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][1] -= 40.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W11_W21_25_H;\n')
					else:
						wires.write('9 trace_cross_W21_W11_25_H;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][1] -= 40.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W21_W11_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_lr'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][0] - limit)

			pos[0][1] += 100.
			pos[1][1] += 100.
			lengthA += 100.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 100.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################


############################################################################################################################
############################################################################################################################
	#Take traces left.
	def d_end(self, wires, bundle_num, pos, edge, twist_flags, next_trace):
		print 'edge is :', edge
		twistA = twist_flags['twistA'] # Flag for how many time we've twisted.
		twistB = twist_flags['twistB'] # Flag for how many time we've twisted.
		twistcountA = twist_flags['twistcountA'] #How many times have we twisted?
		twistcountB = twist_flags['twistcountB'] #How many times have we twisted?
		twistcountA0 = twist_flags['twistcountA0'] #Previous twist count.  If we've upped 1, we need to twist.
		twistcountB0 = twist_flags['twistcountB0']
		lengthA = twist_flags['lengthA']
		lengthB = twist_flags['lengthB']
		space = self.trace_space
		
		#Define the limits for trace growing.
		limit = edge

		cell = 'trace_straight_W11_W21_ud'
		
		#Do we want to twist the pairs?
		#-------------------------------------------------------------------------------------------------------------------
		if self.twist==0: # DON'T TWIST.
			pos[0][1] += 20.
			pos[1][1] += 20.
			wires.write('(SymbolCall ' + cell +');\n')

			limit = edge
			print 'limit=', limit
			diff = abs(pos[0][1] - limit)
			while (pos[0][1] > limit):
				if (diff > 95.):
					pos[0][1] -= 95.
				else:
					pos[0][1] -= diff
				diff = abs(pos[0][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
	
			wires.write('(SymbolCall ' + cell +');\n')

			limit = edge
			print 'limit=', limit
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 95.):
					pos[1][1] -= 95.
				else:
					pos[1][1] -= diff
				diff = abs(pos[1][1] - limit)
				wires.write('9 ' + cell +';\n')
				wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
			pos[0][0] -= 100.
			pos[1][0] -= 100.
			space = self.trace_space
			return pos, edge
		#-------------------------------------------------------------------------------------------------------------------

		#What do we do if we ARE twisting?
		#-------------------------------------------------------------------------------------------------------------------
		else:
			print 'Do the twist.'
			locA = [pos[0][0],pos[0][1]]
			locB = [pos[1][0],pos[1][1]]

			pos[0][1] -= 7.*self.overlap
			pos[1][1] -= 7.*self.overlap

			limit = edge
			diff = abs(pos[0][0] - limit)
			while (pos[0][0] > limit):
				if (diff > 95.):
					pos[0][0] -= 95.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)
				else:
					pos[0][1] -= diff
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

				#Do we need to add a twist?
				if twistcountA - twistcountA0 > 0.25:
					pos[0][1] -= 40.
					locA0 = tuple(locA)
					locA[0],locA[1] = pos[0][0], pos[0][1]
					dlengthA = distance(locA0[0],locA0[1],locA[0],locA[1])
					lengthA += dlengthA
					twistcountA0 = twistcountA
					twistcountA = floor(lengthA/self.twistlengthA)

					if round(mod(twistA,2.)) > 0.25:
						wires.write('9 trace_cross_W11_W21_25_ud;\n')
					else:
						wires.write('9 trace_cross_W21_W11_25_ud;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					twistA += 1.
					pos[0][1] += 40.
				else:
				#Have we twisted?
					if mod(twistA,2.) > 0.25:
						cell = 'trace_straight_W21_W11_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[0][0])) + ' ' + str(int(1000.*pos[0][1])) + ';\n')
				diff = abs(pos[0][0] - limit)

			limit = edge
			diff = abs(pos[1][1] - limit)
			while (pos[1][1] > limit):
				if (diff > 95.):
					pos[1][1] -= 95.
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)
				else:
					pos[1][1] += diff
					locB0 = tuple(locB)
					locB[0],locB[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

			#Do we need to add a twist?
				if twistcountB - twistcountB0 > 0.25:
					pos[1][1] -= 40.
					locB0 = tuple(locB)
					locB[0],locA[1] = pos[1][0], pos[1][1]
					dlengthB = distance(locB0[0],locB0[1],locB[0],locB[1])
					lengthB += dlengthB
					twistcountB0 = twistcountB
					twistcountB = floor(lengthB/self.twistlengthB)

					if round(mod(twistB,2.)) > 0.25:
						wires.write('9 trace_cross_W11_W21_25_V;\n')
					else:
						wires.write('9 trace_cross_W21_W11_25_V;\n')
					wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					twistB += 1.
					pos[1][1] -= 40.
				else:
				#Have we twisted?
					if mod(twistB,2.) > 0.25:				
						cell = 'trace_straight_W21_W11_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
					else:
						cell = 'trace_straight_W11_W21_ud'
						wires.write('9 ' + cell +';\n')
						wires.write('C 0 T ' + str(int(1000.*pos[1][0])) + ' ' + str(int(1000.*pos[1][1])) + ';\n')
				diff = abs(pos[1][0] - limit)

			pos[0][1] -= 100.
			pos[1][1] -= 100.
			lengthA += 100.
			twistcountA0 = twistcountA
			twistcountA = floor(lengthA/self.twistlengthA)

			lengthB += 100.
			twistcountB0 = twistcountB
			twistcountB = floor(lengthB/self.twistlengthB)
			
			#Replace all of the twist flags with their new values.
			twist_flags['twistA'] = twistA 
			twist_flags['twistB'] = twistB
			twist_flags['twistcountA'] = twistcountA
			twist_flags['twistcountB'] = twistcountB
			twist_flags['twistcountA0'] = twistcountA0
			twist_flags['twistcountB0'] = twistcountB0
			twist_flags['lengthA'] = lengthA
			twist_flags['lengthB'] = lengthB
			space = self.trace_space
			return pos, edge, twist_flags
			#---------------------------------------------------------------------------------------------------------------
############################################################################################################################
############################################################################################################################
