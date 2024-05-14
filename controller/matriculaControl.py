from models.persona import Persona
from models.rol import Rol
from models.cuenta import Cuenta
from models.curso import Curso
from models.matricula import Matricula
from models.periodo import Periodo
from app import db
import uuid

class MatriculaControl:
    def guardarMatricula(self, data):
        persona2 = Persona.query.filter_by(external_id=data.get("id_alumno")).first()
        periodo2 = Periodo.query.filter_by(external_id=data.get("id_periodo")).first()
        curso2 = Curso.query.filter_by(external_id=data.get("id_curso")).first()
        if persona2 and periodo2 and curso2:
            matricula = Matricula()
            matricula.fecha = data.get("fecha")
            matricula.id_curso = curso2.id
            matricula.id_alumno = persona2.id
            matricula.id_periodo = periodo2.id
            matricula.external_id = uuid.uuid4()
            if persona2.rol.nombre != 'alumno':
                return -2
            db.session.add(matricula)
            db.session.commit()
        else:
            return -1
        return matricula.id
    
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

    def listarMatricula(self):
        return Matricula.query.all()
    
    def listarPeriodo(self):
        return Periodo.query.all()
    
    def listarCurso(self):
        return Curso.query.all()
