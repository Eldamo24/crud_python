from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__) # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend
# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:090518Zoe@localhost/proyecto'
# URI de la BBDD driver de la BD user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app) #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app) #crea el objeto ma de de la clase Marshmallow
# defino la tabla
class Anime(db.Model): # la clase Anime hereda de db.Model
    id=db.Column(db.Integer, primary_key=True) #define los campos de la tabla
    nombre=db.Column(db.String(100))
    temporadas=db.Column(db.Integer)
    capitulos=db.Column(db.Integer)
    descripcion=db.Column(db.String(400))
    imagen=db.Column(db.String(400))
    def __init__(self,nombre,temporadas,capitulos, descripcion, imagen): #crea el constructor de la clase
        self.nombre=nombre # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.temporadas = temporadas
        self.capitulos = capitulos
        self.descripcion = descripcion
        self.imagen=imagen

# si hay que crear mas tablas , se hace aqui

with app.app_context():
    db.create_all() # aqui crea todas las tablas
# ************************************************************
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

# programa principal *******************************
if __name__=='__main__':
    app.run(debug=True, port=5000) # ejecuta el servidor Flask en el puerto 5000