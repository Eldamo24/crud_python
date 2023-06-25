from app import db, app


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

with app.app_context():
    db.create_all() # aqui crea todas las tablas