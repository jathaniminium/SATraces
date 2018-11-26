# SATraces
Semi-automatic wire trace layout code for use with the Xic mask editing software package.

Many trace element building blocks are defined in `xic_elements`.  The code spits out txt files containing calls to the relevant trace elements.  When compile in Xic and merged, contiguous wire traces are produced.  In this use case, the wire traces connect to microstrip wire pairs exiting a pixel to a bank of bond pads at the edge of a silicon wafer.

This code was written in the fall of 2010 and spring of 2011 to define the wiring layout for pixels in the South Pole Telescope SPTpol receiver's 150 GHz detector wafers.  This work was done while I was a graduate student at the University of Colorado at Boulder in collaboration with the Quantum Sensor Group at NIST-Boulder, who ultimately fabricated the wafers.  It also acted as a concrete project to start practicing coding in python, which I had recently learned.

The bulk of the code exists in `trace_element.py`, which defines trace blocks in various orientations.  The remaining code consists of scripts that generate output files for specific groupings of pixels, for which I desired all the wiring to bundle together with a set spacing between traces and move as a unit.  Each script would define trace routing with a list of directions I required the traces to go on a wafer, as well as how far I needed each trace unit to travel.  Look at `A1_1_1.py` as an example.  The trace routing was hand-defined for each bundle of pixels.  However, the inner-bundle spacing of wire pairs for each detector, the number of trace elements to use to generate a trace of sufficient length, as well whether and how to "twist" wire pairs and keep track of the number of twists were all automated, hence the name "Semi-Automated Traces."

