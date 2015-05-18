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

		with io.open('ArtistList.json', 'w', encoding='utf-8') as f:
  			f.write(unicode(json.dumps(response_data, ensure_ascii=False)))

  	def getTopTracksFromArtist(self,artist):
  		args = {
  			"method":	"artist.getTopTracks",
  			"limit":	10,
  			"artist":	artist
  		}

  		response_data = self.send_request(args)

		with io.open(str(artist) + ".json", 'w', encoding='utf-8') as f:
  			f.write(unicode(json.dumps(response_data, ensure_ascii=False)))

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


		with io.open(str(artist) + "TAGS" + ".json", 'w', encoding='utf-8') as f:
  			f.write(unicode(json.dumps(resp_d, ensure_ascii=False)))


class mongoforlast:
	def __init__(self):
		self.PATH = "D:/MongoDB/Server/3.0/bin/lastJSON/"
		self.USER = "Poobowl"
	
	def insertarBD(path = self.PATH, user = self.USER):
		#configurar la conexion
		cliente = MongoClient()
		db=cliente.proyecto
		dir= os.listdir(path)
		dir.pop
		for x in (dir):
			print(x)
			f = open(path+x, 'r')
			res=db[user].insert_one(eval(f.read()))
			print(res.inserted_id)

	def Transformador(self, user):
		cliente = MongoClient()
		db=cliente.proyecto
		cursor = db[user].find({"toptags.tag":{"$exists" : True}})
		numGeneros=[]
		for document in cursor:
			for genre in document["toptags"]["tag"]:
				numGeneros.append(genre["name"])			
		numGeneros = list(set(numGeneros))
		listGeneros=[]
		for x in numGeneros:
			artistas = db[user].find({"toptags.tag.name":x})
			listArtistas=[]
			for y in artistas:
				canciones = db[user].find({"toptracks.@attr.artist":y["toptags"]["@attr"]["artist"]})
				listCanciones=[]
				for z in canciones[0]["toptracks"]["track"]:
					cancion={"name":z["name"],"group":4}
					listCanciones.append(cancion)
				artista=({"children":listCanciones,"name":y["toptags"]["@attr"]["artist"],"group":3})
				listArtistas.append(artista)
			genero=({"children":listArtistas,"name":x,"group":2})
			listGeneros.append(genero)
		res={"children":listGeneros,"name":user,"group":1}
		print(res)
		print(json.dumps(res))
		f=open("final.json","w")
		f.write(json.dumps(res))
	


@app.route("/")
def indexview():
	last_request = lastfm()
	mongo_request = mongoforlast()

	with io.open("ArtistList.json", 'r', encoding='utf-8') as data_file:
		data = json.load(data_file)

	data_file.close()
	
	for artist in data["topartists"]["artist"]:
		last_request.getTopTags(str(artist["name"]))

	mongo_request.insertarBD("D:/MongoDB/Server/3.0/bin/LASTFMULTIMATE/", "Poobowl")
	mongo_request.Transformador("Poobowl")

	return render_template('index.html')


	
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)


