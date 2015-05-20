#LastFM_Database_Visualization

Autores:
	* Francisco Manuel Morales Carlín
	* David Blanco Cañizares
	* Diego Fariñas Fernández
	* Miguel Castillo Lloret

###About

Esta aplicación permite obtener la colección de música de un usuario de LastFM,
traspasándola a una base de datos noSQL, MongoDB y visualizándola en el navegador
con la ayuda de d3.js

##LastFM

Utilizando la API de LastFM tenemos acceso a todos los datos de la cuenta del usuario,
como obtener los artistas(grupos de musica) de su colección, canciones más populares de estos
o agregar y borrar artistas.

En particular, nosotros hemos hecho uso de:
	* [user.getTopArtists](http://www.lastfm.es/api/show/user.getTopArtists)
	* [artist.getTopTracks](http://www.lastfm.es/api/show/artist.getTopTracks)
	* [artist.getTopTags](http://www.lastfm.es/api/show/artist.getTopTags)

Estos se encargaran de extraer la información en formato JSON la cual formará parte de la
base de datos de MongoDB

##MongoDB

Para facilitar la gestión de de datos hemos elegido MongoDB, la cual es una base de datos *no relacional*
y que trabaja con ficheros BSON, o Binary JSON, (que ya tenemos gracias a la api de lastfm)

Esta base de datos actuará como una *caché*. Es decir, la visualización de datos se realizará a partir de aquí
y no directamente de LastFM, de modo que cuando actualicemos la cuenta de lastfm (como puede ser el agregar un artista)
la base de datos renovará su contenido y por tanto la visualización de éste.

Nos hemos decantado por el módulo *Pymongo* ---Mongo for Python--- que deberá instalar en su equipo para el uso de 
esta aplicación

Más información:
	* [Pymongo](http://api.mongodb.org/python/current/api/)

##d3.js

No deberíamos definirla como una api sino como una librería de javascript ---haciendo uso de WebGL---
que facilita notablemente la creación de distintos layouts con los que representar los datos de forma
gráfica como es el caso del *árbol desplegable* y por medio de un simple JSON `./static/arbol`

Más información:
	* [d3.js](https://github.com/mbostock/d3/wiki)


###Dependencias

Las dependencias de la aplicación pueden instalarse usando:

`$ pip install -r requirements.txt`

