from flask import Flask ,jsonify ,request
from app import app, ma
from modelos import *

class AnimeSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','temporadas','capitulos', 'descripcion','imagen')

anime_schema=AnimeSchema() # El objeto anime_schema es para traer un producto
animes_schema=AnimeSchema(many=True) # El objeto animes_schema es para traer multiples registros de anime

# crea los endpoint o rutas (json)
@app.route('/animes',methods=['GET'])
def get_Animes():
    all_animes=Anime.query.all() # el metodo query.all() lo hereda de db.Model
    result=animes_schema.dump(all_animes) # el metodo dump() lo hereda de ma.schema y

# trae todos los registros de la tabla
    return jsonify(result) # retorna un JSON de todos los registros de la tabla

@app.route('/animes/<id>',methods=['GET'])
def get_Anime(id):
    anime=Anime.query.get(id)
    return anime_schema.jsonify(anime) # retorna el JSON de un anime recibido como parametro

@app.route('/animes/<id>',methods=['DELETE'])
def delete_anime(id):
    anime=Anime.query.get(id)
    db.session.delete(anime)
    db.session.commit()
    return anime_schema.jsonify(anime) # me devuelve un json con el registro eliminado
@app.route('/animes', methods=['POST']) # crea ruta o endpoint
def create_anime():
#print(request.json) # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    temporadas=request.json['temporadas']
    capitulos=request.json['capitulos']
    descripcion=request.json['descripcion']
    imagen=request.json['imagen']
    new_anime=Anime(nombre,temporadas, capitulos, descripcion,imagen)
    db.session.add(new_anime)
    db.session.commit()
    return anime_schema.jsonify(new_anime)
@app.route('/animes/<id>' ,methods=['PUT'])
def update_anime(id):
    anime=Anime.query.get(id)
    anime.nombre=request.json['nombre']
    anime.temporadas=request.json['temporadas']
    anime.capitulos=request.json['capitulos']
    anime.descripcion=request.json['descripcion']
    anime.imagen=request.json['imagen']
    db.session.commit()
    return anime_schema.jsonify(anime)
