from app import db

class Partir_Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    id_docente = db.Column(db.Integer, db.ForeignKey('persona.id'))
    docente = db.relationship('Persona', backref=db.backref('partir_materias', lazy=True))
    id_periodo = db.Column(db.Integer, db.ForeignKey('periodo.id'))
    periodo = db.relationship('Periodo', backref=db.backref('partir_materias', lazy=True))
    id_materia = db.Column(db.Integer, db.ForeignKey('asignatura.id'), nullable=False, unique=True)
    materia = db.relationship('Asignatura', backref=db.backref('partir_materias', uselist=False))
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id'))
    curso = db.relationship('Curso', backref=db.backref('partir_materias', lazy=True))

    def serialize(self):
        # Obtener el nombre del rol asociado
        materia_data = None
        if self.materia:
            materia_data = {
                'nombre': self.materia.nombre,
                'codigo_materia': self.materia.codigo_materia
            }

        docente_data = None
        if self.docente:
            docente_data = {
                'nombre': self.docente.nombre,
                'apellido': self.docente.apellido
            }

        nombre_curso = ""
        if self.curso:
            nombre_curso = self.curso.nombre

        nombre_periodo = ""
        if self.periodo:
            nombre_periodo = self.periodo.descripcion
        
        return  {
            'materia':materia_data,
            'periodo': nombre_periodo,
            'curso': nombre_curso,
            'docente': docente_data,
            'external_id':self.external_id,
        }


