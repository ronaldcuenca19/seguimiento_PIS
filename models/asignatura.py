from app import db

class Asignatura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    codigo_materia = db.Column(db.String(50))
    nombre = db.Column(db.String(50))
    nombre_profesor = db.Column(db.String(100))

    def serialize(self):
        return  {
            'nombre': self.nombre,
            'nombre_profesor': self.nombre_profesor,
            'codigo_materia': self.codigo_materia,
            'external_id':self.external_id,
        }