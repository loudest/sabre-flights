#!/usr/bin/env python
import os, json, xml, getopt, sys, re
from xml.dom.minidom import parse, parseString

def parse(file):
	
	results = []
	i = 0
	for line in open(file,'r').readlines():	
	
		# determine valid flight or not
		boolean = valid_flight(line)
		if(boolean == True):
			flight = {}
			flight['segments'] = []
			flight['fares'] = []
			xml = parseString(line)
			
			#print line
			
			# parse segments
			segments = xml.getElementsByTagName("FlightSegment")
			for segment in segments:
				segment_array = {}
				segment_array['Origin'] = segment.getAttribute("Origin")
				segment_array['Destination'] = segment.getAttribute("Destination")
				segment_array['CarrierCode'] = segment.getAttribute("CarrierCode")
				segment_array['FlightNumber'] = segment.getAttribute("FlightNumber")
				segment_array['DepartureDateTime'] = segment.getAttribute("DepartureDateTime")
				segment_array['ArrivalDateTime'] = segment.getAttribute("ArrivalDateTime")
				segment_array['BookingCode'] = segment.getAttribute("BookingCode")
				segment_array['CabinClass'] = segment.getAttribute("CabinClass")
				segment_array['SeatsRemaining'] = segment.getAttribute("SeatsRemaining")
				flight['segments'].append(segment_array)
				
			# parse fares
			fares = xml.getElementsByTagName("Fare")
			for fare in fares:
				fare_array = {}
				fare_array['PassengerCode'] = fare.getAttribute("PassengerCode")
				fare_array['BaseAmount'] = fare.getAttribute("BaseAmount")
				fare_array['TaxAmount'] = fare.getAttribute("TaxAmount")
				fare_array['Currency'] = fare.getAttribute("Currency")
				fare_array['Refundable'] = fare.getAttribute("Refundable")
				fare_array['ETicketable'] = fare.getAttribute("ETicketable")
				flight['fares'].append(fare_array)
				
			
			results.append(flight)
			# one liner
			if i > 20:
				print results
				sys.exit(0)
			else:
				i = i + 1

def valid_flight(line):
	if "AirItinerary" in line:
		return True
	else:
		return None

def usage():
    print "./extract.py -f <target>-h]"
    print " -f|--file <file to parse>"
    print " -h|--help Shows this help\n"
	
def main(argv):
   
    try:
        opts, args = getopt.getopt(argv, "hf:", ["help", "file="])
    except getopt.GetoptError:
        usage()
        sys.exit(-1)

	file = None
	
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        if o in ("f", "--file"):
            file = a

	if file == None:
		usage()
		sys.exit(-1)
		
	parse(file)
	
if __name__ == "__main__":
    main(sys.argv[1:])	

	