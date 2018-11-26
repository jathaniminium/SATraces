#from trace_element_dev import trace_element_dev  as trace_element
from trace_element import trace_element
from numpy import *
from pf import pf

name = 'A1_1_1'
bundle_num = 1.
start1 = pf['JNR']
start2 = pf['TESA45']

pixel_offset = [pf[name][0], pf[name][1]]
location = [pixel_offset[0]*pf['dx'], pixel_offset[1]*pf['dy']]
wires = open(r'/Users/jathaniminium/xic/sptpol6_traces/traces/'+name+'.txt', 'w')
wires.write('(Traces for ' + name + ');\n')

pos = [[location[0] + start1[0] + 1000., location[1] + start1[1]],
       [location[0] + start2[0] + 1000., location[1] + start2[1]]] # or up/down test traces.

#List of elements and element boundaries for this trace.  In practice, this is all you'll have to change for every pixel.
element_list = ['dr45start', 'dr45d', 'd', 'dl', 'l', 'lul45', 'ul45', 'ul45u',
                'u', 'uul45', 'ul45', 'ul45u',
                'u', 'uul45', 'ul45', 'ul45l', 
                'l_end','stop']

boundaries = [0.,  0.,  location[1] + start2[1] - 1000. - 350., 0., -6750., 0., pf['A1_1_1b'][1] -2600., 0.,
              -21000. - 731. - 20., 0., pf['A1_1_4b'][1] - 2500. - 50.*6. - 400. + 155. + 500., 0.,
              pf['A1_1_4b'][1] - 1000. + 50. - 50.*12. + 247.990 - 421., 0., pf['A1_1_4b'][1] + 100. - 50., 0., 
              -17995. + 280. + 85., 0.]

############################################################################################################################
################Beginning of element writing script.  No editing required below this point##################################
############################################################################################################################
#Reset some parameters that change as the trace grows.
twist_flags = {'twistA':0., # Flag for how many times we've twisted.
			   'twistB':0., # Flag for how many times we've twisted.
			   'twistcountA':0.,  #How many times have we twisted?
			   'twistcountB':0.,  #How many times have we twisted?
			   'twistcountA0':0., #Previous twist count.  If we've upped 1, we need to twist.
			   'twistcountB0':0.,
			   'lengthA':0.,
			   'lengthB':0.
			   }

#Load in trace element class with parameter file.
element = trace_element(pf)
#Do a loop over all trace elements.
for i in range(len(element_list) -1):
	#load in the limit boundary for this element.
	edge = boundaries[i]
	next_trace = element_list[i+1]
	print 'Position is:', pos
	
	#Is there a better way to change call the function?  Can you edit the name of the function as a string?
	if element_list[i] == 'u':
		element.u(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'd':
		element.d(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'l':
		element.l(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'r':
		element.r(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] =='ur':
		element.ur(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'ru':
		element.ru(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'dr':
		element.dr(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'rd':
		element.rd(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'ul':
		element.ul(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'lu':
		element.lu(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'dl':
		element.dl(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'ld':
		element.ld(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'ur45':
		element.ur45(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'dr45':
		element.dr45(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'ul45':
		element.ul45(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'dl45':
		element.dl45(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'ur45u':
		element.ur45u(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'ur45r':
		element.ur45r(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'ul45u':
		element.ul45u(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'ul45l':
		element.ul45l(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'dr45d':
		element.dr45d(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'dr45r':
		element.dr45r(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'dl45d':
		element.dl45d(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'dl45l':
		element.dl45l(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'ldl45':
		element.ldl45(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'rdr45':
		element.rdr45(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'ddl45':
		element.ddl45(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'uul45':
		element.uul45(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'ddr45':
		element.ddr45(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'uur45':
		element.uur45(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'rur45':
		element.rur45(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'ur45r':
		element.ur45r(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'lul45':
		element.lul45(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'dr45start':
		element.dr45start(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'l_end':
		element.l_end(wires, bundle_num, pos, edge, twist_flags, next_trace)
	elif element_list[i] == 'r_end':
		element.r_end(wires, bundle_num, pos, edge, twist_flags, next_trace)
wires.close()
