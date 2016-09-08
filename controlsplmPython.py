from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse
import SocketServer
import urllib2
import json
import os
import csv
from time import gmtime, strftime

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
		if self.path == '/part':
			print "Inside PART request"
			content_length = int(self.headers['Content-Length']) # Gets the size of data
			partData = self.rfile.read(content_length) # Gets the data itself
			partJson = json.loads(partData)
			partCSVData = partJson['part']
			currentTime = strftime("%Y%m%d%H%M%S", gmtime())
			partFileName = 'partCSV_'+currentTime+'.csv'
			
			# PART CSV generation begins expecting JSON as input 
			headers = ["CELL", "ITEM-NUM", "DESCRIPTION", "PM-CODE", "UM", "REV", "DRAWING-NBR", "ALT-ITEM", "PROD-FAM", "PHANTOM", "MATL-TYPE", "UNIT-WEIGHT","WEIGHT-UNITS", 
						"COUNTRY OF ORIGIN", "BA-FLG", "BUY-AMERICAN-XREF-PROD-ID", "ITEM-ST", "STD-COST", "ASM-FIXED", "COMP-FIXED", "BTO", "COMM-CODE", "YR-USG", "YR-FCST",
						"SALES-LT", "MIN-CUST", "PACK-QTY", "PACK-TYPE", "PLAN-ID", "PLN-CDE", "ORD-MIN", "ORD-MULT", "MSP", "STK-WHSE", "ATO", "SSTK", "SUB", "STD-LT", "BUY-ID",
						"PRD-SRC", "RANK", "VEND-NUM", "NAME", "VEND-ITEM", "VEND-UM", "CONV-FA", "VLT", "BRK-QTY", "BRK-COST", "BRK-DATE", "MLT", "NCRET", "EXT-ABC", "RVEFFPUR", 
						"FLT", "AUTOREP", "ACCEPT", "REPLDYS"]
			output = csv.DictWriter(open(partFileName,'w'), delimiter=',', lineterminator='\n', fieldnames=headers) 
			output.writerow(dict((fn,fn) for fn in headers))
			output.writerows(partCSVData)			
			self.send_response(200)
			self.end_headers()

		if self.path == '/bom':
			print "Inside BOM request"
			content_length = int(self.headers['Content-Length']) 
			bomData = self.rfile.read(content_length)
			bomJson = json.loads(bomData)
			bomCSVData = bomJson['bom']
			currentTime = strftime("%Y%m%d%H%M%S", gmtime())
			bomFileName = 'bomCSV_'+currentTime+'.csv'
			
			# BOM CSV generation begins expecting JSON as input 
			headers = ["END-ITEM", "ACTION", "SEQ", "MAT-ITEM", "MATL-QTY", "UNITS", "START-EFF-DATE", "END-EFF_DATE"]
			output = csv.DictWriter(open(bomFileName,'w'), delimiter=',', lineterminator='\n', fieldnames=headers) 
			output.writerow(dict((fn,fn) for fn in headers))
			output.writerows(bomCSVData)			
			self.send_response(200)
			self.end_headers()
        
def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print 'Server started http://127.0.0.1:8000/'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()