from flask import Blueprint, jsonify, make_response, request
from controller.materiaControl import MateriaControl
from flask_expects_json import expects_json
from controller.authenticate import token_required
from controller.utiles.errores import Errors

api_materia = Blueprint('api_materia', __name__)
materiaC = MateriaControl()

schema_materia = {
    'type': 'object',
    'properties': {
        'nombre': {'type': 'string'},
        'id_docente': {'type': 'string'},
    },
    'required': ['nombre', 'id_docente']
}

schema_partirmateria = {
    'type': 'object',
    'properties': {
        'id_docente': {'type': 'string'},
        'id_periodo': {'type': 'string'},
        'id_curso': {'type': 'string'},
        'id_materia': {'type': 'string'},
    },
    'required': ['id_docente', 'id_periodo', 'id_curso','id_materia']
}

@api_materia.route('/materia/save', methods=["POST"])
@token_required
@expects_json(schema_materia)
def create():
    data = request.json
    materia_id = materiaC.guardarMateria(data)
    if materia_id == -1:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-3)]}}
            ),
            401,
        )
    elif materia_id == -2:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-4)]}}
            ),
            401,
        )
    else:
        return make_response(
            jsonify({"msg":"OK", "code":200, "data": materia_id}),
            200,
        )

@api_materia.route('/partir_materia/save', methods=["POST"])
@token_required
@expects_json(schema_partirmateria)
def createpartir_materia():
    data = request.json
    materia_id = materiaC.partirMateria(data)
    if materia_id == -1:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-3)]}}
            ),
            401,
        )
    elif materia_id == -2:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-4)]}}
            ),
            401,
        )
    elif materia_id == -3:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-10)]}}
            ),
            401,
        )
    else:
        return make_response(
            jsonify({"msg":"OK", "code":200, "data": materia_id}),
            200,
        )
    
@api_materia.route("/materia", methods=["GET"])
def listMateria():
    datos_materia = materiaC.listarMateria()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_materia])}),
        200
    )

@api_materia.route("/materia/<external>", methods=["GET"])
def listMateriaDocente(external):
    datos_materia = materiaC.listarMateria_Docente(external)
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_materia])}),
        200
    )

@api_materia.route("/partir_materia", methods=["GET"])
def listPartirMateria():
    datos_partirmateria = materiaC.listarPartir_Materia()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_partirmateria])}),
        200
    )