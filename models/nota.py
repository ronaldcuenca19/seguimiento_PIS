from app import db
from sqlalchemy import Enum, CheckConstraint

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    nota_total = db.Column(db.Float)
    fecha_registro = db.Column(db.Date)
    nombre_alumno = db.Column(db.String(100))
    id_unidad = db.Column(db.Integer, db.ForeignKey('unidad.id'))
    unidad = db.relationship('Unidad', backref=db.backref('notas', lazy=True))
    id_materia = db.Column(db.Integer, db.ForeignKey('asignatura.id'))
    materia = db.relationship('Asignatura', backref=db.backref('notas', lazy=True))

    def serialize(self):
        # Obtener el nombre del rol asociado
        materia_data = None
        if self.materia:
            materia_data = {
                'nombre': self.materia.nombre,
                'codigo_materia': self.materia.nombre_profesor
            }

        unidad_data = None
        if self.unidad:
            unidad_data = {
                'nombre': self.unidad.nombre
            }
        
        return  {
            'nota_total':self.nota_total,
            'fecha_registro': self.fecha_registro,
            'nombre_alumno': self.nombre_alumno,
            'unidad': unidad_data,
            'materia': materia_data,
            'external_id':self.external_id,
        }
