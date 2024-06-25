from models.persona import Persona
from models.rol import Rol
from models.cuenta import Cuenta
from models.partir_materia import Partir_Materia
from models.nota import Nota
from models.asignatura import Asignatura
from models.informe_nota import Informe_Nota
from models.unidad import Unidad
from models.curso import Curso
from models.periodo import Periodo
from app import db
from sqlalchemy.exc import IntegrityError
import re
import uuid
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

class PersonaControl:

    def inicio_sesion(self, data):
        accountA = Cuenta.query.filter_by(correo=data["correo"]).first()
        if accountA:
            #decrypt password
            if check_password_hash(accountA.clave, data["clave"]):
                expire_time = datetime.now() + timedelta(minutes=30)
                token_payload = {
                    "external_id": accountA.external_id,
                    "expire": expire_time.strftime("%Y-%m-%d %H:%M:%S") 
                }
                print('-------------', token_payload)
                token = jwt.encode(
                    token_payload,
                    key=current_app.config["SECRET_KEY"],
                    algorithm="HS512"
                )    
                person = accountA.getPerson(accountA.id_persona)
                user_info = {
                    "token": token,
                    "user": person.apellido + " " + person.nombre,
                    "external": person.external_id,
                    "rol": person.rol.nombre
                }
                return user_info
            else:
                -6
        else:
            return -6
        
    def guardarUsuario(self, data, rol):
        roles2 = Rol.query.filter_by(nombre=rol).first()
        contraseña_sin_hashear = data.get("clave")
        contraseña_hasheada = generate_password_hash(contraseña_sin_hashear)
        print('caqui1', roles2.nombre)
        persona = Persona()
        persona.apellido = data.get("apellidos")
        persona.nombre = data.get("nombres")
        persona.edad = data.get("edad")
        persona.cedula = data.get("cedula")
        persona.external_id = uuid.uuid4()
        persona.estado = data.get("estado")
        persona.id_rol = roles2.id
        cuenta = Cuenta()
        cuenta.correo = data.get("correo")
        cuenta.clave = contraseña_hasheada
        cuenta.external_id = uuid.uuid4()
        persona.cuenta = cuenta

        if not PersonaControl.validar_correo(cuenta.correo):
            db.session.rollback()
            return None

        cuentas_existentes = Cuenta.query.all()
        for cuenta_existente in cuentas_existentes:
            if cuenta_existente.correo == cuenta.correo:
                db.session.rollback()
                return None

        try:
            db.session.add(persona)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  
            return -8

        return persona.id

    def validar_correo(correo):
        patron = r"^[a-zA-Z0-9\.\-]+@[a-zA-Z0-9\.\-]+[.][a-zA-Z]*$"
        if re.match(patron, correo):
            return True
        else:
            return False

    def listar(self):
        return Persona.query.all()
    

    def actualizarUsuario(self, data):
        persona = Persona.query.filter_by(external_id=data.get("id_persona")).first()
        if persona:
            persona.apellido = data.get("apellidos", persona.apellido)
            persona.nombre = data.get("nombres", persona.nombre)
            persona.edad = data.get("edad", persona.edad)
            persona.cedula = data.get("cedula", persona.cedula)
            persona.estado = data.get("estado", persona.estado)
            db.session.merge(persona)
            db.session.commit()
        else:
            return -1

        return persona.id
    
    def bajarPersona (self,  external):
        personita = Persona.query.filter_by(external_id=external).first()
        if personita is None:
            return -1
        else:
            cuenta2 = personita.cuenta
            cuenta2.estado = False
            db.session.commit()
        return personita

    
    




