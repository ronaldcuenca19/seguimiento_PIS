from models.persona import Persona
from models.rol import Rol
from models.partir_materia import Partir_Materia
from models.cuenta import Cuenta
from models.curso import Curso
from models.matricula import Matricula
from models.asignatura import Asignatura
from models.periodo import Periodo
from app import db
from flask import jsonify
import uuid
import random
import string
from sqlalchemy.exc import IntegrityError

class MateriaControl:
    def guardarMateria(self, data):
        profesor2 = Persona.query.filter_by(external_id=data.get("id_docente")).first()
        if profesor2:
            if profesor2.rol.nombre == 'docente':
                materia = Asignatura()
                materia.nombre_profesor = profesor2.nombre + '' + profesor2.apellido
                materia.nombre = data.get("nombre")
                materia.codigo_materia = MateriaControl.generar_codigo_unico()
                materia.external_id = uuid.uuid4()
                db.session.add(materia)
                db.session.commit()
            else:
                return -2
        else:
            return -1
        return materia.id

    def partirMateria(self, data):
        profesor2 = Persona.query.filter_by(external_id=data.get("id_docente")).first()
        materia2 = Asignatura.query.filter_by(external_id=data.get("id_materia")).first()
        periodo2 = Periodo.query.filter_by(external_id=data.get("id_periodo")).first()
        curso2 = Curso.query.filter_by(external_id=data.get("id_curso")).first()

        if curso2 and profesor2 and materia2 and periodo2:
            if profesor2.rol.nombre == 'docente':
                partir_materia = Partir_Materia()
                partir_materia.id_periodo = periodo2.id
                partir_materia.id_materia = materia2.id
                partir_materia.id_docente = profesor2.id
                partir_materia.id_curso = curso2.id
                partir_materia.external_id = uuid.uuid4()

                try:
                    db.session.add(partir_materia)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    return -3
            else:
                return -2  # El profesor no tiene el rol adecuado
        else:
            return -1  # Falta uno o más datos necesarios

        return partir_materia.id

    
    def generar_codigo_unico():
        longitud = 6  # Longitud del código
        caracteres = string.ascii_uppercase + string.digits  # Letras mayúsculas y dígitos
        codigo = ''.join(random.choices(caracteres, k=longitud))  # Generar código aleatorio
        return codigo
    
    def listarMateria(self):
        return Asignatura.query.all()
    
    def listarPartir_Materia(self):
        return Partir_Materia.query.all()