from models.persona import Persona
from models.rol import Rol
from models.cuenta import Cuenta
from models.curso import Curso
from models.periodo import Periodo
from app import db
import uuid

class MatriculaControl:    
    def guardarPeriodo(self, data):
        periodo = Periodo()
        periodo.fecha_inicio = data.get("fecha_inicio")
        periodo.fecha_fin = data.get("fecha_fin")
        periodo.descripcion = data.get("descripcion")
        periodo.external_id = uuid.uuid4()
        db.session.add(periodo)
        db.session.commit()
        return periodo.id

    def guardarCurso(self, data):
        curso = Curso()
        curso.Paralelo = data.get("paralelo")
        curso.nombre = data.get("nombre")
        curso.external_id = uuid.uuid4()
        db.session.add(curso)
        db.session.commit()
        return curso.id
    
    def listarPeriodo(self):
        return Periodo.query.all()
    
    def listarCurso(self):
        return Curso.query.all()
