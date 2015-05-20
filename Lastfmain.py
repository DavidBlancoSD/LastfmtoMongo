#!/usr/bin/python
# -*- coding: utf-8 -*-

from pprint import pprint
import urllib, urllib2
import inspect
import io
import os
from flask import Flask, render_template
from flask import request
from pymongo import MongoClient
try:
	import json
except ImportError:
	import simplejson as json

app = Flask(__name__)

class lastfm:
	def __init__(self):
		self.API_URL = "http://ws.audioscrobbler.com/2.0/"
		self.API_KEY = "6c8a3809178c98317933a66b03b4a8fc"

	def send_request(self, args, **kwargs):
		kwargs.update(args)
		kwargs.update({
			"api_key":	self.API_KEY,
			"format":	"json"
		})
		try:
			url = self.API_URL + "?" + urllib.urlencode(kwargs)
			data = urllib2.urlopen(url)
			response_data = json.load(data)
			data.close()

			return response_data
		except urllib2.HTTPError, e:
			print "HTTPError: %d" % e.code
		except urllib2.URLError, e:
			print "Network error: %s" % e.reason.args[1]

	def getArtistFromUser(self):
		args = {
			"method":	"user.getTopArtists",
			"user":		"Poobowl",
			"limit":	30

		}

		response_data = self.send_request(args)

		return response_data

  	def getTopTracksFromArtist(self,artist):
  		args = {
  			"method":	"artist.getTopTracks",
  			"limit":	10,
  			"artist":	artist
  		}

  		response_data = self.send_request(args)

  		ruta = './lastJSON'
  		if not os.path.exists(ruta):
  			os.makedirs(ruta)

		with io.open(ruta + "/" + str(artist) + "TAGS" + ".json", 'w', encoding='utf-8') as f:
  			f.write(unicode(json.dumps(resp_d, ensure_ascii=False)))

  	def getTopTags(self, artist):
  		args = {
  			"method":	"artist.getTopTags",
  			"artist":	artist
  		}

  		response_data = self.send_request(args)

  		resp_d ={"toptags":{"tag":response_data["toptags"]["tag"][0:7],"@attr":response_data["toptags"]["@attr"]}}
  	
  		for suparr in resp_d.values():
  			for tag in suparr["tag"]:
  				tag["name"] = tag["name"].replace('-','').replace(' ','').upper()


		ruta = './lastJSON'
  		if not os.path.exists(ruta):
  			os.makedirs(ruta)

		with io.open(ruta + "/" + str(artist) + "TAGS" + ".json", 'w', encoding='utf-8') as f:
  			f.write(unicode(json.dumps(resp_d, ensure_ascii=False)))


class mongoforlast:
	def __init__(self):
		self.PATH = "./lastJSON/"
		self.USER = "Poobowl"

	def insertarBD(self):
		cliente = MongoClient()
		db = cliente.proyecto
		dir = os.listdir(self.PATH)
		dir.pop
		for archivo in (dir):
			print (archivo)
			f = open(self.PATH + archivo, 'r')
			res = db[self.USER].insert_one(eval(f.read()))
			print(res.inserted_id)

	def transformador(self):
		cliente = MongoClient()
		db = cliente.proyecto
		cursor = db[self.USER].find({"toptags.tag":{"$exists" : True}})
		numGeneros=[]
		for document in cursor:
			for genre in document["toptags"]["tag"]:
				numGeneros.append(genre["name"])			
		numGeneros = list(set(numGeneros))
		listGeneros=[]
		for x in numGeneros:
			artistas = db[self.USER].find({"toptags.tag.name":x})
			listArtistas=[]
			for y in artistas:
				canciones = db[self.USER].find({"toptracks.@attr.artist":y["toptags"]["@attr"]["artist"]})
				listCanciones=[]
				for z in canciones[0]["toptracks"]["track"]:
					cancion={"name":z["name"],"group":4}
					listCanciones.append(cancion)
				artista=({"children":listCanciones,"name":y["toptags"]["@attr"]["artist"],"group":3})
				listArtistas.append(artista)
			genero=({"children":listArtistas,"name":x,"group":2})
			listGeneros.append(genero)
		res={"children":listGeneros,"name":self.USER,"group":1}
		print(res)
		print(json.dumps(res))
		f=open("./static/arbol.json","w")
		f.write(json.dumps(res))




@app.route("/")
def view_index():

	return render_template('index.html')


@app.route("/lastfmtomongotod3")
def main_work():
	last_request = lastfm()
	mongo_request = mongoforlast()

	data = last_request.getArtistFromUser()

	for artist in data["topartists"]["artist"]:
		last_request.getTopTracksFromArtist(str(artist["name"]))
		last_request.getTopTags(str(artist["name"]))


	mongo_request.insertarBD()	
	mongo_request.transformador()

	return render_template('index.html')

	
if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000,debug=True)
	


