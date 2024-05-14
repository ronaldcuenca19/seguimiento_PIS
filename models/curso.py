from app import db

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    nombre = db.Column(db.String(60))
    Paralelo = db.Column(db.String(40))

    def serialize(self):        
        return  {
            'nombre': self.nombre,
            'paralelo': self.Paralelo,
            'external_id':self.external_id,
        }
