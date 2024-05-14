from flask import Blueprint, jsonify, make_response, request
from controller.personaControl import PersonaControl
from controller.matriculaControl import MatriculaControl
from flask_expects_json import expects_json
from controller.authenticate import token_required
from controller.utiles.errores import Errors

api_api = Blueprint('api_api', __name__)
personaC = PersonaControl()
matriculaC = MatriculaControl()

schema = {
    'type': 'object',
    'properties': {
        'nombres': {'type': 'string'},
        'apellidos': {'type': 'string'},
        'edad': {'type': 'string'},
        'correo': {'type': 'string'},
        'clave': {'type': 'string'},
        'cedula':{'type': 'string'},
        'estado': {'type': 'string'},
    },
    'required': ['nombres', 'apellidos', 'edad', 'correo', 'clave', 'estado', 'cedula']
}

schema2 = {
    'type': 'object',
    'properties': {
        'id_persona': {'type': 'string'},
        'nombres': {'type': 'string'},
        'apellidos': {'type': 'string'},
        'edad': {'type': 'string'},
        'cedula':{'type': 'string'},
        'estado': {'type': 'string'},
    },
    'required': ['nombres', 'apellidos', 'edad', 'estado', 'cedula', 'id_persona']
}

schema_matricula = {
    'type': 'object',
    'properties': {
        'fecha': {'type': 'string', 'format': 'date-time'}, 
        'id_curso': {'type': 'string'},
        'id_periodo': {'type': 'string'},
        'id_alumno':{'type': 'string'},
    },
    'required': ['fecha', 'id_curso', 'id_periodo', 'id_alumno']
}

schema_periodo = {
    'type': 'object',
    'properties': {
        'fecha_inicio': {'type': 'string', 'format': 'date-time'}, 
        'fecha_fin': {'type': 'string', 'format': 'date-time'},
        'descripcion': {'type': 'string'},
    },
    'required': ['fecha_inicio', 'fecha_fin', 'descripcion']
}

schema_curso = {
    'type': 'object',
    'properties': {
        'paralelo': {'type': 'string'}, 
        'nombre': {'type': 'string'},
    },
    'required': ['paralelo', 'nombre']
}

schema_session = {
    "type": "object",
    "properties": {
        "correo": {"type": "string"},
        "clave": {"type": "string"},
    },
    "required": ["correo", "clave"],
}

@api_api.route("/persona/cambiarEstado/<external>", methods=["GET"])
@token_required
def cambiarEstado( external):
    # Aquí se obtiene el parámetro 'external' de la URL y se pasa a la función 'listarPersona'
    id = personaC.bajarPersona(external)
    if id == -1:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-3)]}}
            ),
            401,
        )
    else:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos":()}),
            200
        )

@api_api.route("/login", methods=["POST"])
@expects_json(schema_session)
def session():
    data = request.json
    id = personaC.inicio_sesion(data)
    if (type(id)) == int:
        return make_response(
            jsonify(
                {"msg": "ERROR", "code": 400, "data": {"error": Errors.error[str(id)]}}
            ),
            400,
        )
    else:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "data": {"tag": id}}), 200
        )

@api_api.route('/persona/save/admin', methods=["POST"])
@token_required
@expects_json(schema)
def create():
    data = request.json
    person_id = personaC.guardarUsuario (data,'admin')
    if person_id != -8:
        return make_response(
            jsonify({"msg":"OK", "code":200, "data": person_id}),
            200,
        )
    else:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-8)]}}
            ),
            401,
        )

@api_api.route('/persona/save/docente', methods=["POST"])
@token_required
@expects_json(schema)
def create_docente():
    data = request.json
    person_id = personaC.guardarUsuario (data,'docente')
    if person_id != -8:
        return make_response(
            jsonify({"msg":"OK", "code":200, "data": person_id}),
            200,
        )
    else:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-8)]}}
            ),
            401,
        )
    
@api_api.route('/persona/save/alumno', methods=["POST"])
@token_required
@expects_json(schema)
def create_estudiante():
    data = request.json
    person_id = personaC.guardarUsuario (data,'alumno')
    if person_id != -8:
        return make_response(
            jsonify({"msg":"OK", "code":200, "data": person_id}),
            200,
        )
    else:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-8)]}}
            ),
            401,
        )
    
@api_api.route('/persona/modificar', methods=["POST"])
@token_required
@expects_json(schema2)
def update():
    data = request.json
    person_id = personaC.actualizarUsuario (data)
    if person_id != -1:
        return make_response(
            jsonify({"msg":"OK", "code":200, "data": person_id}),
            200,
        )
    else:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-3)]}}
            ),
            401,
        )
    

@api_api.route('/matricula/save', methods=["POST"])
@token_required
@expects_json(schema_matricula)
def create_matricula():
    data = request.json
    matricula_id = matriculaC.guardarMatricula (data)
    if matricula_id == -1:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-3)]}}
            ),
            401,
        )
    elif matricula_id == -2:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-4)]}}
            ),
            401,
        )
    else:
        return make_response(
            jsonify({"msg":"OK", "code":200, "data": matricula_id}),
            200,
        )
    
@api_api.route('/periodo/save', methods=["POST"])
@token_required
@expects_json(schema_periodo)
def create_periodo():
    data = request.json
    periodo_id = matriculaC.guardarPeriodo (data)
    return make_response(
            jsonify({"msg":"OK", "code":200, "data": periodo_id}),
            200,
        )

@api_api.route('/curso/save', methods=["POST"])
@token_required
@expects_json(schema_curso)
def create_curso():
    data = request.json
    curso_id = matriculaC.guardarCurso (data)
    return make_response(
            jsonify({"msg":"OK", "code":200, "data": curso_id}),
            200,
        )
    
@api_api.route("/persona", methods=["GET"])
@token_required
def list():
    # Aquí se obtiene el parámetro 'external' de la URL y se pasa a la función 'listarPersona'
    datos_persona = personaC.listar()
    
    # Se verifica si se encontró una persona con el external_id dado
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_persona])}),
        200
    )

@api_api.route("/matricula", methods=["GET"])
@token_required
def listMatricula():
    # Aquí se obtiene el parámetro 'external' de la URL y se pasa a la función 'listarPersona'
    datos_matricula = matriculaC.listarMatricula()
    
    # Se verifica si se encontró una persona con el external_id dado
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_matricula])}),
        200
    )

@api_api.route("/periodo", methods=["GET"])
def listPeriodo():
    # Aquí se obtiene el parámetro 'external' de la URL y se pasa a la función 'listarPersona'
    datos_periodo = matriculaC.listarPeriodo()
    
    # Se verifica si se encontró una persona con el external_id dado
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_periodo])}),
        200
    )

@api_api.route("/curso", methods=["GET"])
def listCurso():
    # Aquí se obtiene el parámetro 'external' de la URL y se pasa a la función 'listarPersona'
    datos_curso= matriculaC.listarCurso()
    
    # Se verifica si se encontró una persona con el external_id dado
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_curso])}),
        200
    )
