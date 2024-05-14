from app import db
from sqlalchemy import Enum, CheckConstraint

class Periodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    descripcion = db.Column(db.String(100))

    def serialize(self):        
        return  {
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'descripcion': self.descripcion,
            'external_id':self.external_id,
        }