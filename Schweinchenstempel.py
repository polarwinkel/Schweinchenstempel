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

namen = 'Ole,Erik,Lasse'
anzahl = '5'

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
    page = '<html><head><title>Schweinchen- und Sternchenstempel</title><style>body{font-family: Arial, Helvetica, sans-serif;}</style></head>\n<body>\n'
    data = yaml.load(open(schweinchenfile, 'r'))
    for kind in kinder:
        page = page+'<h1>'+kind+'</h1>\n'
        page = page+getSchweinchen(kind, data[kind])
        page = page+'<form method="post" enctype="text/plain"><button name="Schweinchen" value="%s"><img src="Schweinchen.svg" height="150px" /></button>'% kind
        page = page+'<button name="Sternchen" value="%s"><img src="Sternchen.svg" height="150px" /></button></form>'% kind
    page = page+'<form method="post" enctype="text/plain"><button name="reset" value="true">Reset</button></form>'
    page = page+'<body></html>'
    return bytes(page, 'utf8')

def getSchweinchen(name, data):
    ''' Creates the Schweinchen-Content depending on the saved Schweinchen '''
    # TODO: Schweinchen in yml-Datei speichern (mit Datum)
    ergebnis = ''
    for s in data['Schweinchen']:
        ergebnis = ergebnis+'<img src="Schweinchen.svg" height="150px" />'
    ergebnis = ergebnis+'<br />\n'
    for s in data['Sternchen']:
        ergebnis = ergebnis+'<img src="Sternchen.svg" height="150px" />'
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
            data[kind]['Schweinchen'].append('TODO: Zeitstempel neues Schweinchen')
            yaml.safe_dump(data, open(schweinchenfile, 'w'))
        elif 'Sternchen='+kind in post_data:
            data[kind]['Sternchen'].append('TODO: Zeitstempel neues Sternchen')
            yaml.safe_dump(data, open(schweinchenfile, 'w'))

class Handler(http.server.SimpleHTTPRequestHandler):
    ''' Handler to serve the Website and get the POST-data '''
    
    def do_GET(self):
        ''' return page on GET-request '''
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        if self.path.endswith(".svg"):
            f=open('.'+self.path, 'rb')
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
