import glob
import argparse
import random
import json
import re
import multiprocessing
from urllib.request import Request, urlopen
import urllib.parse



class Rosetta:

	_urlBase 	= 'https://www.letsmt.eu/ws/service.svc/json/GetSystemList?appID=myappid'
	_tranUrl 	= 'https://www.letsmt.eu/ws/service.svc/json/Translate?appID=myappid&systemID=__CORPUSID__&text=__TEXT__'
	_token   	= ''
	_langid  	= ''
	_translate	= ''


	# 0 Spanish - English (NMT) Lynx
	# 1 Greek - English Generic NMT
	#....
	# 9 English - Spanish (NMT) Lynx
	#... Así hasta diez valores.
	#Se pasa en transalte ese valor para ver el corpusId

	def __init__( self, token, translate = 'Spanish - English (NMT) Lynx'):
		self._token = token
		self._translate = translate		

	def connect (self):

		request = Request( self._urlBase )
		request.add_header('client-id', self._token )

		content = urlopen(request)

		if content.status==200:
			data = json.load (content)

			for d in data['System']:
				if d['Metadata'][0]['Value'] == self._translate:
					self._langid = d['ID']
					print ('identificador de idioma %s ' % self._langid)
					self._tranUrl = self._tranUrl.replace ('__CORPUSID__', self._langid)
					print (self._tranUrl)
		else:
			print ('no se ha podido cargar la API, %s' % content.status)

		return ([content.status, self._langid])

	def translate (self, text):
		url = self._tranUrl.replace ('__TEXT__', urllib.parse.quote(text) )
		request = Request( url )
		request.add_header('client-id', self._token)
		content = urlopen(request)

		return ([content.status, content.read().decode()])




if __name__ == "__main__":


	myR = Rosetta (token = 'u-fc6f1588-4dc0-4358-aa48-106749f327af', translate = 'English - Spanish (NMT) Lynx')
	
	if myR.connect()[0] == 200:
		text = "For those unfamiliar with the Analogue Pocket, it's a handheld device that looks like a modern Game Boy. Well, it basically is a Game Boy. It includes custom computing hardware to play any official Game Boy, Game Boy Color and Game Boy Advance cartridge. It also works with carts from other handheld gaming systems, like Game Gear and Neo Geo Pocket Color. For those with no interest in gaming, don't worry, there's a digital photography angle on the way."

		data1 = myR.translate (text)
	else:
		print ('error')

	import ipdb ; ipdb.set_trace()
	

'''


token = 'u-fc6f1588-4dc0-4358-aa48-106749f327af'
url = 'https://www.letsmt.eu/ws/service.svc/json/GetSystemList?appID=myappid'


request = Request( url )
request.add_header('client-id', token)


content = urlopen(request)

if content.status==200:
	data = json.load (content)

	for d in data['System']:
		if d['Metadata'][0]['Value'] == 'Spanish - English (NMT) Lynx':
			langid = d['ID']
			print ('identificador de idioma %s ' % langid)
else:
	print ('no se ha podido cargar la API, %s' % content.status)


text = 'hola a todo el mundo, hace un día maravilloso'


url = 'https://www.letsmt.eu/ws/service.svc/json/Translate?appID=myappid&systemID=' + langid + '&text=' + urllib.parse.quote(text)
request = Request( url )
request.add_header('client-id', token)



import ipdb ; ipdb.set_trace()


'''