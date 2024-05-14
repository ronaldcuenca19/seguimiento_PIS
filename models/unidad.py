from app import db

class Unidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    nombre = db.Column(db.String(50))

    def serialize(self):
        return  {
            'fecha_inicio':self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'nombre': self.nombre,
            'external_id':self.external_id,
        }