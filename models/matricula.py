from app import db
from sqlalchemy import Enum, CheckConstraint

class Matricula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    fecha = db.Column(db.Date)
    id_periodo = db.Column(db.Integer, db.ForeignKey('periodo.id'), nullable=False, unique=True)
    periodo = db.relationship('Periodo', backref=db.backref('matriculas', lazy=True))
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id'))
    curso = db.relationship('Curso', backref=db.backref('matriculas', lazy=True))
    id_alumno = db.Column(db.Integer, db.ForeignKey('persona.id'))
    alumno = db.relationship('Persona', backref=db.backref('matriculas', lazy=True))

    def serialize(self):
        alumno_data = None
        if self.alumno:
            alumno_data = {
                'nombre': self.alumno.nombre, 
                'apellido':self.alumno.apellido                
            }

        nombre_curso = ""
        if self.curso:
            nombre_curso = self.curso.nombre

        nombre_periodo = ""
        if self.periodo:
            nombre_periodo = self.periodo.descripcion
        
        return  {
            'fecha': self.fecha,
            'curso': nombre_curso,
            'alumno': alumno_data,
            'periodo': nombre_periodo,
            'external_id':self.external_id,
        }
