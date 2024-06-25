from models.persona import Persona
from models.rol import Rol
from models.partir_materia import Partir_Materia
from models.cuenta import Cuenta
from models.curso import Curso
from models.asignatura import Asignatura
from models.nota import Nota
from models.unidad import Unidad
from models.informe_nota import Informe_Nota
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from app import db
from sqlalchemy import and_
import uuid

class NotaControl:
    def guardarUnidad(self, data):
        unidad = Unidad()
        fecha_inicio = data.get("fecha_inicio")
        fecha_fin = data.get("fecha_fin")

        if fecha_fin < fecha_inicio:
            return -1

        unidad.fecha_inicio = fecha_inicio
        unidad.fecha_fin = fecha_fin
        unidad.nombre = data.get("nombre")
        unidad.external_id = uuid.uuid4()
        db.session.add(unidad)
        db.session.commit()
        return unidad.id
    
    def guardarNota(self, data):
        unidad2 = Unidad.query.filter_by(external_id = data.get("id_unidad")).first()
        materia2 = Asignatura.query.filter_by(external_id = data.get("id_materia")).first()
        if unidad2 and materia2:
            nota = Nota()
            nota.nota_total = data.get("nota_total")
            nota.fecha_registro = datetime.now().date()
            nota.nombre_alumno = data.get("nombre_alumno")
            nota.id_unidad = unidad2.id
            nota.id_materia = materia2.id
            nota.external_id = uuid.uuid4()
            db.session.add(nota)
            db.session.commit()
        else:
                return -1
        return nota.id
    
    def guardarInforme_Nota(self, data):
        nota2 = Nota.query.filter_by(external_id=data.get("id_nota")).first()
        if nota2:
            informe_nota = Informe_Nota()
            informe_nota.Leccion = data.get("leccion")
            informe_nota.Evaluacione = data.get("evaluacion")
            informe_nota.Practica = data.get("practica")
            informe_nota.Deber = data.get("deber")
            informe_nota.id_nota = nota2.id
            informe_nota.external_id = uuid.uuid4()
            try:
                db.session.add(informe_nota)
                db.session.commit()
                external2 = data.get("id_nota")
                self.calcularPromedioTotal(informe_nota, external2)
            except IntegrityError:
                db.session.rollback()
                return -2
        else:
            return -1
        return informe_nota.id
    
    def calcularPromedioTotal(self, informe_nota, id_nota):
        leccion_porc = 0.20
        evaluacion_porc = 0.35
        practica_porc = 0.25
        deber_porc = 0.20
        promedio_total = (informe_nota.Leccion * leccion_porc) + (informe_nota.Evaluacione * evaluacion_porc) + (informe_nota.Practica * practica_porc) + (informe_nota.Deber * deber_porc)
        nota = Nota.query.filter_by(external_id=id_nota).first()
        nota.nota_total = promedio_total
        db.session.merge(nota)
        db.session.commit()
        return promedio_total
    
    def listarUnidad(self):
        return Unidad.query.all()
    
    def listarNota(self):
        return Nota.query.all()
    
    def listarNotaDetalle(self, external):
        materia2 = Asignatura.query.filter_by(external_id = external).first()
        return Nota.query.filter_by(id_materia=materia2.id).all()
    
    def listarInformeNota(self):
        return Informe_Nota.query.all()
    

    def EliminarNotas(self, external, valor):
        materia2 = Asignatura.query.filter_by(external_id=external).first()
        unidad2 = Unidad.query.filter_by(external_id=valor).first()
        try:
            notas = Nota.query.filter(and_(Nota.id_materia == materia2.id, Nota.id_unidad == unidad2.id)).all() 
            for nota in notas:
                db.session.delete(nota)  # Eliminar cada nota
            db.session.commit()  # Confirmar los cambios en la base de datos
            return True, "Notas eliminadas correctamente."
        except Exception as e:
            db.session.rollback()  # Revertir cualquier cambio pendiente en caso de error
            return False, f"Error al eliminar notas: {str(e)}"
        

    def listar_Notas_Materia_Unidad(self, external, valor):
        materia2 = Asignatura.query.filter_by(external_id=external).first()
        unidad2 = Unidad.query.filter_by(external_id=valor).first()
        return Nota.query.filter(and_(Nota.id_materia == materia2.id, Nota.id_unidad == unidad2.id)).all() 

