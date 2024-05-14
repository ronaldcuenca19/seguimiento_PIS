from flask import Blueprint, jsonify, make_response, request
from controller.notaControl import NotaControl
from flask_expects_json import expects_json
from controller.authenticate import token_required
from controller.utiles.errores import Errors

api_nota = Blueprint('api_nota', __name__)
notaC = NotaControl()

schema_unidad = {
    'type': 'object',
    'properties': {
        'nombre': {'type': 'string'},
        'fecha_inicio': {'type': 'string', 'format': 'date-time'},
        'fecha_fin': {'type': 'string', 'format': 'date-time'}
    },
    'required': ['nombre', 'fecha_inicio', 'fecha_fin']
}

schema_nota = {
    'type': 'object',
    'properties': {
        'id_unidad': {'type': 'string'},
        'id_materia': {'type': 'string'},
        'id_alumno': {'type': 'string'},
    },
    'required': ['id_unidad', 'id_materia', 'id_alumno']
}

schema_informe_nota = {
    'type': 'object',
    'properties': {
        'deber': {'type': 'number', 'minimum': 0, 'maximum': 10},  
        'leccion': {'type': 'number', 'minimum': 0, 'maximum': 10}, 
        'evaluacion': {'type': 'number', 'minimum': 0, 'maximum': 10},  
        'practica': {'type': 'number', 'minimum': 0, 'maximum': 10},  
        'id_nota': {'type': 'string'},
    },
    'required': ['deber', 'leccion', 'evaluacion', 'practica', 'id_nota']
}

@api_nota.route('/unidad/save', methods=["POST"])
@token_required
@expects_json(schema_unidad)
def createUnidad():
    data = request.json
    unidad_id = notaC.guardarUnidad(data)
    if unidad_id == -1:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-9)]}}
            ),
            401,
        )
    else:
        return make_response(
            jsonify({"msg":"OK", "code":200, "data": unidad_id}),
            200,
        )

@api_nota.route('/nota/save', methods=["POST"])
@token_required
@expects_json(schema_nota)
def createNota():
    data = request.json
    nota_id = notaC.guardarNota(data)
    if nota_id == -1:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-3)]}}
            ),
            401,
        )
    elif nota_id == -2:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-11)]}}
            ),
            401,
        )
    else:
        return make_response(
            jsonify({"msg":"OK", "code":200, "data": nota_id}),
            200,
        )
    
@api_nota.route('/informe_nota/save', methods=["POST"])
@token_required
@expects_json(schema_informe_nota)
def createInformeNota():
    data = request.json
    informe_nota_id = notaC.guardarInforme_Nota(data)
    if informe_nota_id == -1:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-3)]}}
            ),
            401,
        )
    elif informe_nota_id == -2:
        return make_response(
            jsonify(
                {"msg":"Error", "code":401, "data": {"error": Errors.error[str(-12)]}}
            ),
            401,
        )
    else:
        return make_response(
            jsonify({"msg":"OK", "code":200, "data": informe_nota_id}),
            200,
        )
    
@api_nota.route("/unidad", methods=["GET"])
def listUnidad():
    datos_unidad = notaC.listarUnidad()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_unidad])}),
        200
    )

@api_nota.route("/nota", methods=["GET"])
@token_required
def listNota():
    datos_nota = notaC.listarNota()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_nota])}),
        200
    )

@api_nota.route("/informe_nota", methods=["GET"])
@token_required
def listInforNota():
    datos_informe_nota = notaC.listarInformeNota()
    
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos":([i.serialize() for i in datos_informe_nota])}),
        200
    )