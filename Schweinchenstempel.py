#!/bin/python3
# This file is part of the free Software Schweinchenstempel.
# It is (c) 2018 under the WTFPL Version 2.0:

#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                   Version 2, December 2004
# 
#Copyright (C) 2018 Dirk Winkel <it@polarwinkel.de>
#
#Everyone is permitted to copy and distribute verbatim or modified
#copies of this license document, and changing it is allowed as long
#as the name is changed.
# 
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
# 0. You just DO WHAT THE FUCK YOU WANT TO.

import http.server
import socketserver
from http import HTTPStatus
from collections import OrderedDict
import yaml
import os
import datetime

namen = 'Ole,Erik,Lasse'
#anzahl = '5'

port = 2121
schweinchenfile = 'schweinchen.yml'

kinder = ['']

def parseNamen():
    ''' parst die Namen in eine List '''
    i = 0
    for char in namen:
        if char == ',':
            kinder.append('')
            i += 1
        else:
            kinder[i] = kinder[i]+char

def reset():
    ''' create empty Schweinchen-yml-file '''
    data = {'Ole': {'Schweinchen': [], 'Sternchen': []}, 'Erik': {'Schweinchen': [], 'Sternchen': []}, 'Lasse': {'Schweinchen': [], 'Sternchen': []}}
    yaml.safe_dump(data, open(schweinchenfile, 'w'))

def createPage():
    ''' Create the HTML-Page based on the saved data '''
    page = '<!doctype html><html><head><title>Schweinchen- und Sternchenstempel</title><style>body{font-family: Arial, Helvetica, sans-serif;}</style></head>\n<body>\n'
    data = yaml.load(open(schweinchenfile, 'r'))
    for kind in kinder:
        page = page+'<h1 style="font-size:50px; margin:0; padding-bottom:0;">'+kind+'</h1>\n'
        page = page+getSchweinchen(kind, data[kind])
        page = page+'<form method="post" enctype="text/plain">\n'
        page = page+'<button name="Schweinchen" value="%s"><p style="font-size:50px; margin:0;">+1<img src="Schweinchen.svg" height="60px" /></p></button>\n'% kind
        page = page+'<button name="Sternchen" value="%s"><p style="font-size:50px; margin:0;">+1<img src="Sternchen.svg" height="60px" /></p></button><br />\n'% kind
        page = page+'</form><br />\n'
        page = page+'<hr>'
    page = page+'<form method="post" enctype="text/plain"><button name="reset" value="true"><p style="font-size:50px; margin:0;">Reset</p></button></form>\n'
    page = page+'</body></html>'
    return bytes(page, 'utf8')

def getSchweinchen(name, data):
    ''' Creates the Schweinchen-Content depending on the saved Schweinchen '''
    ergebnis = ''
    for s in data['Schweinchen']:
        ergebnis = ergebnis+'<figure style="float:left;"><img src="Schweinchen.svg" height="120px" alt="%s" />'% s
        ergebnis = ergebnis+'<figcaption>%s</figcaption></figure>\n'% s
    ergebnis = ergebnis+'<br style="clear:both" />\n'
    for s in data['Sternchen']:
        ergebnis = ergebnis+'<figure style="float:left;"><img src="Sternchen.svg" height="120px" alt="%s"/>'% s
        ergebnis = ergebnis+'<figcaption>%s</figcaption></figure>\n'% s
    ergebnis = ergebnis+'<br style="clear:both" />'
    return ergebnis

def changeSchweinchen(post_data):
    ''' change the Schweinchen-yml according to the post_data '''
    print(post_data)
    if 'reset=true' in post_data:
        reset()
        return
    data = yaml.load(open(schweinchenfile, 'r'))
    for kind in kinder:
        if 'Schweinchen='+kind in post_data:
            data[kind]['Schweinchen'].append('{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
            yaml.safe_dump(data, open(schweinchenfile, 'w'))
        elif 'Sternchen='+kind in post_data:
            data[kind]['Sternchen'].append('{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
            yaml.safe_dump(data, open(schweinchenfile, 'w'))

class Handler(http.server.SimpleHTTPRequestHandler):
    ''' Handler to serve the Website and get the POST-data '''
    
    def do_GET(self):
        ''' return page on GET-request '''
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        if self.path.endswith(".svg"):
            f=open(os.path.basename(self.path), 'rb')
            self.wfile.write(f.read())
            f.close()
        else:
            self.wfile.write(createPage())
    
    def do_POST(self):
        ''' get the POST-Data and give feedback if it is fine to work with '''
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        changeSchweinchen(str(post_data, 'utf8'))
        self.wfile.write(createPage())

parseNamen()
if os.path.dirname(__file__) != '':
	os.chdir(os.path.dirname(__file__))
if not os.path.isfile(schweinchenfile):
	reset() 
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(('', port), Handler)
httpd.serve_forever()
