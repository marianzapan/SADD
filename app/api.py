from flask import request, jsonify, make_response
from base64 import b64decode
from pymongo.collection import ReturnDocument
from pymongo.command_cursor import CommandCursor
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from gridfs import GridFSBucket, GridFS
from mimetypes import guess_type
from json import loads
from app import app
from app.model import *
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import datetime

db = client.sadd_db
bucket = GridFSBucket(db)
file_manager = GridFS(db)

#-----------------------------------------------------------------------------------------------------------------
#GET

@app.route('/api/proveedores', methods=['GET'])
@app.route('/api/proveedores/<id>', methods=['GET'])
@jwt_required()
def getFP(id=None):
    if chkPermissions(get_jwt_identity(), 'fp', 'r'):
        num_factura = request.args.get('num_factura')
        xml = request.args.get('xml')
        pdf = request.args.get('pdf')
        if id: res = db.fp.find_one({"_id" : ObjectId(id)})
        elif num_factura: res = db.fp.find_one({"num_factura" : num_factura})
        else: res = db.fp.aggregate([
                { "$unwind": "$num_registro" },
                { "$lookup": {
                        "from": "catalogo",
                        "localField": "num_registro",
                        "foreignField": "num_registro",
                        "as": "registro"
                } },
                { "$unwind": "$registro" }
            ])

        if xml: res = db.fp.find_one({"xml" : ObjectId(xml)})
        if pdf: res = db.fp.find_one({"pdf" : ObjectId(pdf)})

        if res:
            if type(res) is CommandCursor: temp = [getData(i) for i in res]
            else: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response(jsonify("No tiene permiso para realizar esta acción."), 403)

@app.route('/api/clientes', methods=['GET'])
@app.route('/api/clientes/<id>', methods=['GET'])
@jwt_required()
def getFC(id=None):
    if chkPermissions(get_jwt_identity(), 'fc', 'r'):
        num_factura = request.args.get('num_factura')
        xml = request.args.get('xml')
        pdf = request.args.get('pdf')
        if id: res = db.fc.find_one({"_id" : ObjectId(id)})
        elif num_factura: res = db.fc.find_one({"num_factura" : num_factura})
        else: res = db.fc.aggregate([
                { "$unwind": "$num_registro" },
                { "$lookup": {
                        "from": "catalogo",
                        "localField": "num_registro",
                        "foreignField": "num_registro",
                        "as": "registro"
                } },
                { "$unwind": "$registro" }
            ])

        if xml: res = db.fc.find_one({"xml" : ObjectId(xml)})
        if pdf: res = db.fc.find_one({"pdf" : ObjectId(pdf)})

        if res:
            if type(res) is CommandCursor: temp = [getData(i) for i in res]
            else: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response(jsonify("No tiene permiso para realizar esta acción."), 403)

@app.route('/api/catalogo', methods=['GET'])
@app.route('/api/catalogo/<id>', methods=['GET'])
@jwt_required()
def getCatalogo(id=None):
    if chkPermissions(get_jwt_identity(), 'catalogo', 'r'):
        tipo = request.args.get('tipo')
        num_registro = request.args.get('num_registro')
        if id: res = db.catalogo.find_one({"_id" : ObjectId(id)})
        elif tipo: res = db.catalogo.find_one({"tipo" : tipo})
        elif num_registro: res = db.catalogo.find_one({"num_registro" : num_registro})
        else: res = db.catalogo.find({})
        if res:
            if type(res) is Cursor: temp = [getData(i) for i in res]
            else: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/pedimentos', methods=['GET'])
@app.route('/api/pedimentos/<id>', methods=['GET'])
@jwt_required()
def getPedimentos(id=None):
    if chkPermissions(get_jwt_identity(), 'pedimentos', 'r'):
        doc = request.args.get('doc')
        num_pedimento = request.args.get('num_pedimento')
        if doc: res = db.pedimentos.find_one({"doc" : ObjectId(doc)})
        elif id: res = db.pedimentos.find_one({"_id" : ObjectId(id)})
        elif num_pedimento: res = db.pedimentos.find_one({"num_pedimento" : num_pedimento})
        else: res = db.pedimentos.find({})
        if res:
            if type(res) is Cursor: temp = [getData(i) for i in res]
            else: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/packinglists', methods=['GET'])
@app.route('/api/packinglists/<id>', methods=['GET'])
@jwt_required()
def getPackingList(id=None):
    if chkPermissions(get_jwt_identity(), 'pl', 'r'):
        num_ref = request.args.get('num_ref')
        doc = request.args.get('doc')
        img = request.args.get('img')
        if id: res = db.pl.find_one({"_id" : ObjectId(id)})
        elif num_ref: res = db.pl.find_one({"num_ref" : num_ref})
        else: res = db.pl.aggregate([
                { "$unwind": "$num_registro" },
                { "$lookup": {
                        "from": "catalogo",
                        "localField": "num_registro",
                        "foreignField": "num_registro",
                        "as": "registro"
                } },
                { "$unwind": "$registro" }
            ])

        if doc: res = db.pl.find_one({"doc" : ObjectId(doc)})
        if img: res = db.pl.find_one({"img" : ObjectId(img)})

        if res:
            if type(res) is CommandCursor: temp = [getData(i) for i in res]
            else: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/archivos', methods=['GET'])
@app.route('/api/archivos/<id>', methods=['GET'])
@jwt_required()
def getArchivos(id=None):
    if chkPermissions(get_jwt_identity(), 'archivos', 'r'):
        num_ref = request.args.get('num_ref')
        doc = request.args.get('doc')
        if doc: res = db.archivos.find_one({"doc" : ObjectId(doc)})
        elif id: res = db.archivos.find_one({"_id" : ObjectId(id)})
        elif num_ref: res = db.archivos.find_one({"num_ref" : num_ref})
        else: res = db.archivos.aggregate([
                { "$unwind": "$doc" },
                { "$lookup": {
                        "from": "fs.files",
                        "localField": "doc",
                        "foreignField": "_id",
                        "as": "datos"
                } },
                { "$unwind": "$datos" }
            ])
        if res:
            if type(res) is CommandCursor: temp = [getData(i) for i in res]
            else: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/usuarios', methods=['GET'])
@app.route('/api/usuarios/<id>', methods=['GET'])
@jwt_required()
def getUsuario(id=None):
    if chkPermissions(get_jwt_identity(), 'usuarios', 'r'):
        user = request.args.get('user')
        if id: res = db.usuarios.find_one({"_id" : ObjectId(id)})
        elif user: res = db.usuarios.find_one({"user" : user})
        else: res = db.usuarios.find({})
        if res:
            if type(res) is Cursor: temp = [getData(i) for i in res]
            else: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

#-----------------------------------------------------------------------------------------------------------------
#POST

@app.route('/api/proveedores', methods=['POST'])
@jwt_required()
def postFP():
    if chkPermissions(get_jwt_identity(), 'fp', 'c'):
        datos = setData(loads(request.data))
        model = FP()
        model.num_factura = datos['num_factura']
        model.fecha_factura = datos['fecha_factura']
        model.num_registro = datos['num_registro']
        model.num_pedimento = datos['num_pedimento']
        model.fecha_venc = datos['fecha_venc']
        model.xml = b64decode(datos['xml']) if datos['xml'] != 'None' and datos['xml'] != None else None
        model.pdf = b64decode(datos['pdf']) if datos['pdf'] != 'None' and datos['pdf'] != None else None
        id = model.save().inserted_id
        
        if model.xml != None: setFilename(model.xml._id, datos['xml_filename'])
        if model.pdf != None: setFilename(model.pdf._id, datos['pdf_filename'])
        res = db.fp.find_one({"_id":id})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response(jsonify("No tiene permiso para realizar esta acción."), 403)

@app.route('/api/clientes', methods=['POST'])
@jwt_required()
def postFC():
    if chkPermissions(get_jwt_identity(), 'fc', 'c'):
        datos = setData(loads(request.data))
        model = FC()
        model.num_factura = datos['num_factura']
        model.fecha_factura = datos['fecha_factura']
        model.num_registro = datos['num_registro']
        model.num_pedimento = datos['num_pedimento']
        model.xml = b64decode(datos['xml']) if datos['xml'] != 'None' and datos['xml'] != None else None
        model.pdf = b64decode(datos['pdf']) if datos['pdf'] != 'None' and datos['pdf'] != None else None
        id = model.save().inserted_id
        if model.xml != None: setFilename(model.xml._id, datos['xml_filename'])
        if model.pdf != None: setFilename(model.pdf._id, datos['pdf_filename'])
        res = db.fc.find_one({"_id":id})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response(jsonify("No tiene permiso para realizar esta acción."), 403)

@app.route('/api/catalogo', methods=['POST'])
@jwt_required()
def postCatalogo():
    if chkPermissions(get_jwt_identity(), 'catalogo', 'c'):
        datos = setData(loads(request.data))
        model = Catalogo()
        model.num_registro = datos['num_registro']
        model.tipo = datos['tipo']
        model.num_registro = datos['num_registro']
        model.nom = datos['nom']
        model.dir = datos['dir']
        model.tel = datos['tel']
        model.rfc = datos['rfc']
        model.correo = datos['correo']
        id = model.save().inserted_id
        res = db.catalogo.find_one({"_id":id})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response(jsonify("No tiene permiso para realizar esta acción."), 403)

@app.route('/api/pedimentos', methods=['POST'])
@jwt_required()
def postPedimentos():
    if chkPermissions(get_jwt_identity(), 'pedimentos', 'c'):
        datos = setData(loads(request.data))
        model = Pedimentos()
        model.num_pedimento = datos['num_pedimento']
        model.fecha_pedimento = datos['fecha_pedimento']
        model.fecha_venc = datos['fecha_venc']
        model.material = datos['material']
        model.aduana = datos['aduana']
        model.exportador = datos['exportador']
        model.doc = b64decode(datos['doc']) if datos['doc'] != 'None' and datos['doc'] != None else None

        id = model.save().inserted_id
        if model.doc != None:
            setFilename(model.doc._id, datos['doc_filename'])
            setMimeFile(model.doc._id, datos['doc_filename'])

        res = db.pedimentos.find_one({"_id":id})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response(jsonify("No tiene permiso para realizar esta acción."), 403)

@app.route('/api/packinglists', methods=['POST'])
@jwt_required()
def postPackingList():
    if chkPermissions(get_jwt_identity(), 'pl', 'c'):
        datos = setData(loads(request.data))
        model = PL()
        model.num_ref = datos['num_ref']
        model.num_registro = datos['num_registro']
        model.fecha_recibido = datos['fecha_recibido']
        model.fecha_enviado = datos['fecha_enviado']
        model.doc = b64decode(datos['doc']) if datos['doc'] != 'None' and datos['doc'] != None else None
        model.img = b64decode(datos['img']) if datos['img'] != 'None' and datos['img'] != None else None

        id = model.save().inserted_id
        if model.doc != None:
            setFilename(model.doc._id, datos['doc_filename'])
            setMimeFile(model.doc._id, datos['doc_filename'])
        if model.img != None:
            setFilename(model.img._id, datos['img_filename'])
            setMimeFile(model.img._id, datos['img_filename'])
            
        res = db.pl.find_one({"_id":id})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response(jsonify("No tiene permiso para realizar esta acción."), 403)

@app.route('/api/archivos', methods=['POST'])
@jwt_required()
def postArchivo():
    if chkPermissions(get_jwt_identity(), 'archivos', 'c'):
        datos = setData(loads(request.data))
        model = Archivos()
        model.num_ref = datos['num_ref']
        model.fecha = datos['fecha']
        model.desc = datos['desc']
        model.doc = b64decode(datos['doc']) if datos['doc'] != 'None' and datos['doc'] != None else None

        id = model.save().inserted_id
        if model.doc != None:
            setFilename(model.doc._id, datos['doc_filename'])
            setMimeFile(model.doc._id, datos['doc_filename'])
            
        res = db.archivos.find_one({"_id":id})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response(jsonify("No tiene permiso para realizar esta acción."), 403)

@app.route('/api/usuarios', methods=['POST'])
@jwt_required()
def postUsuario():
    if chkPermissions(get_jwt_identity(), 'usuarios', 'c'):
        datos = setData(loads(request.data))
        model = Usuarios()
        model.asignacion = datos['asignacion']
        model.user = datos['user']
        model.password = datos['password']
        model.roles = datos['roles']
        id = model.save().inserted_id
        res = db.usuarios.find_one({"_id":id})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response(jsonify("No tiene permiso para realizar esta acción."), 403)

@app.route('/api/login', methods=['POST'])
def chkUsuario():
    data = loads(request.data)
    user = data['user']
    password = data['password']
    if db.usuarios.find_one({"user" : user, "password" : password}):
        token = create_access_token(identity=user)
        return jsonify(token)
    else: return make_response("El usuario y/o contraseña son erróneos", 422)

@app.route('/api/reporte/<tipo>', methods=['POST'])
@jwt_required()
def generarReporte(tipo):
    data = loads(request.data)
    temp = list()
    if ('fecha_inicio' and 'fecha_fin') not in data:
        if ('fecha_recibido_inicio' and 'fecha_recibido_fin') not in data:
            return make_response("Los datos son insuficientes para generar el reporte.", 422)
    
    data['fecha_inicio'] = datetime.strptime(data['fecha_inicio'], "%Y-%m-%d")
    data['fecha_fin'] = datetime.strptime(data['fecha_fin'], "%Y-%m-%d")

    if 'proveedor' not in data: data['proveedor'] = ""
    if 'cliente' not in data: data['cliente'] = ""
    if 'fecha_venc' not in data: data['fecha_venc'] = ""

    if tipo == 'fp': 
        if (data['proveedor'] != ""): res = db.fp.find({"num_registro": data['proveedor']})
        else: res = res = db.fp.aggregate([
                { "$unwind": "$num_registro" },
                { "$lookup": {
                        "from": "catalogo",
                        "localField": "num_registro",
                        "foreignField": "num_registro",
                        "as": "registro"
                } },
                { "$unwind": "$registro" }
            ])
        for r in res:
            if (data['fecha_inicio'] <= datetime.strptime(r['fecha_factura'], "%Y-%m-%d") <= data['fecha_fin']): 
                temp.append(getData(r))

    if tipo == 'fc':
        if (data['cliente'] != ""): res = db.fc.find({"num_registro": data['cliente']})
        else: res = res = db.fc.aggregate([
                { "$unwind": "$num_registro" },
                { "$lookup": {
                        "from": "catalogo",
                        "localField": "num_registro",
                        "foreignField": "num_registro",
                        "as": "registro"
                } },
                { "$unwind": "$registro" }
            ])
        for r in res:
            if (data['fecha_inicio'] <= datetime.strptime(r['fecha_factura'], "%Y-%m-%d") <= data['fecha_fin']): 
                temp.append(getData(r))

    if tipo == 'pedimentos':
        if (data['fecha_venc'] != ""): res = db.pedimentos.find({"fecha_venc": data['fecha_venc']})
        else: res = db.pedimentos.find({})
        for r in res:
            if (data['fecha_inicio'] <= datetime.strptime(r['fecha_pedimento'], "%Y-%m-%d") <= data['fecha_fin']): 
                temp.append(getData(r))

    if tipo == 'pl':
        if ('fecha_recibido_inicio' and 'fecha_recibido_fin') in data:
            data['fecha_inicio'] = data['fecha_recibido_inicio']
            data['fecha_fin'] = data['fecha_recibido_fin']

        if ('fecha_enviado_inicio' and 'fecha_enviado_fin') not in data:
            return make_response("Los datos son insuficientes para generar el reporte.", 422)

        data['fecha_enviado_inicio'] = datetime.strptime(data['fecha_enviado_inicio'], "%Y-%m-%d")
        data['fecha_enviado_fin'] = datetime.strptime(data['fecha_enviado_fin'], "%Y-%m-%d")
        
        if (data['proveedor'] != ""): res = db.pl.find({"num_registro": data['proveedor']})
        else: res = db.pl.aggregate([
                { "$unwind": "$num_registro" },
                { "$lookup": {
                        "from": "catalogo",
                        "localField": "num_registro",
                        "foreignField": "num_registro",
                        "as": "registro"
                } },
                { "$unwind": "$registro" }
            ])
        for r in res:
            if (data['fecha_inicio'] <= datetime.strptime(r['fecha_recibido'], "%Y-%m-%d") <= data['fecha_fin'] and
                data['fecha_enviado_inicio'] <= datetime.strptime(r['fecha_enviado'], "%Y-%m-%d") <= data['fecha_enviado_fin']): 
                temp.append(getData(r))

    if tipo == 'archivos':
        res = db.archivos.aggregate([
                { "$unwind": "$doc" },
                { "$lookup": {
                        "from": "fs.files",
                        "localField": "doc",
                        "foreignField": "_id",
                        "as": "datos"
                } },
                { "$unwind": "$datos" }
            ])
        for r in res:
            if (data['fecha_inicio'] <= datetime.strptime(r['fecha'], "%Y-%m-%d") <= data['fecha_fin']): 
                temp.append(getData(r))

    return jsonify(temp)

#-----------------------------------------------------------------------------------------------------------------
#PUT / UPDATE

@app.route('/api/proveedores/<id>', methods=['PUT'])
@jwt_required()
def putFP(id):
    if chkPermissions(get_jwt_identity(), 'fp', 'u'):
        datos = setData(loads(request.data))
        res = db.fp.find_one_and_update({'_id':ObjectId(id)}, {'$set': datos}, return_document=ReturnDocument.AFTER)
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/clientes/<id>', methods=['PUT'])
@jwt_required()
def putFC(id):
    if chkPermissions(get_jwt_identity(), 'fc', 'u'):
        datos = setData(loads(request.data))
        res = db.fc.find_one_and_update({'_id':ObjectId(id)}, {'$set': datos}, return_document=ReturnDocument.AFTER)
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/catalogo/<id>', methods=['PUT'])
@jwt_required()
def putCatalogo(id):
    if chkPermissions(get_jwt_identity(), 'catalogo', 'u'):
        datos = setData(loads(request.data))
        res = db.catalogo.find_one_and_update({'_id':ObjectId(id)}, {'$set': datos}, return_document=ReturnDocument.AFTER)
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/pedimentos/<id>', methods=['PUT'])
@jwt_required()
def putPedimento(id):
    if chkPermissions(get_jwt_identity(), 'pedimentos', 'u'):
        datos = setData(loads(request.data))
        res = db.pedimentos.find_one_and_update({'_id':ObjectId(id)}, {'$set': datos}, return_document=ReturnDocument.AFTER)
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/packinglists/<id>', methods=['PUT'])
@jwt_required()
def putPL(id):
    if chkPermissions(get_jwt_identity(), 'pl', 'u'):
        datos = setData(loads(request.data))
        res = db.pl.find_one_and_update({'_id':ObjectId(id)}, {'$set': datos}, return_document=ReturnDocument.AFTER)
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/archivos/<id>', methods=['PUT'])
@jwt_required()
def putArchivo(id):
    if chkPermissions(get_jwt_identity(), 'archivos', 'u'):
        datos = setData(loads(request.data))
        res = db.archivos.find_one_and_update({'_id':ObjectId(id)}, {'$set': datos}, return_document=ReturnDocument.AFTER)
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/usuarios/<id>', methods=['PUT'])
@jwt_required()
def putUsuario(id):
    if chkPermissions(get_jwt_identity(), 'usuarios', 'u'):
        datos = setData(loads(request.data))
        res = db.usuarios.find_one_and_update({'_id':ObjectId(id)}, {'$set': datos}, return_document=ReturnDocument.AFTER)
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

#-----------------------------------------------------------------------------------------------------------------
#DELETE
@app.route('/api/proveedores/<id>', methods=['DELETE'])
@jwt_required()
def delFP(id):
    if chkPermissions(get_jwt_identity(), 'fp', 'd'):
        elem = db.fp.find_one({"_id":ObjectId(id)})
        if elem['xml'] != 'None' and elem['xml'] != None: delFile(elem['xml'])
        if elem['pdf'] != 'None' and elem['xml'] != None: delFile(elem['pdf'])
        res = db.fp.find_one_and_delete({'_id':ObjectId(id)})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/clientes/<id>', methods=['DELETE'])
@jwt_required()
def delFC(id):
    if chkPermissions(get_jwt_identity(), 'fc', 'd'):
        elem = db.fc.find_one({"_id":ObjectId(id)})
        if elem['xml'] != 'None' and elem['xml'] != None: delFile(elem['xml'])
        if elem['pdf'] != 'None' and elem['pdf'] != None: delFile(elem['pdf'])
        res = db.fc.find_one_and_delete({'_id':ObjectId(id)})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/clientes/<id>', methods=['DELETE'])
@jwt_required()
def delCatalogo(id):
    if chkPermissions(get_jwt_identity(), 'catalogo', 'd'):
        res = db.catalogo.find_one_and_delete({'_id':ObjectId(id)})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/pedimentos/<id>', methods=['DELETE'])
@jwt_required()
def delPedimento(id):
    if chkPermissions(get_jwt_identity(), 'pedimentos', 'd'):
        elem = db.pedimentos.find_one({"_id":ObjectId(id)})
        if elem['doc'] != 'None' and elem['doc'] != None: delFile(elem['doc'])
        res = db.pedimentos.find_one_and_delete({'_id':ObjectId(id)})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/packinglists/<id>', methods=['DELETE'])
@jwt_required()
def delPL(id):
    if chkPermissions(get_jwt_identity(), 'pl', 'd'):
        elem = db.pl.find_one({"_id":ObjectId(id)})
        if elem['doc'] != 'None' and elem['doc'] != None: delFile(elem['doc'])
        if elem['doc'] != 'None' and elem['img'] != None: delFile(elem['img'])
        res = db.pl.find_one_and_delete({'_id':ObjectId(id)})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/archivos/<id>', methods=['DELETE'])
@jwt_required()
def delArchivo(id):
    if chkPermissions(get_jwt_identity(), 'archivos', 'd'):
        elem = db.archivos.find_one({"_id":ObjectId(id)})
        if elem['doc'] != 'None' and elem['doc'] != None: delFile(elem['doc'])
        res = db.archivos.find_one_and_delete({'_id':ObjectId(id)})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

@app.route('/api/usuarios/<id>', methods=['DELETE'])
@jwt_required()
def delUsuario(id):
    if chkPermissions(get_jwt_identity(), 'usuarios', 'd'):
        res = db.usuarios.find_one_and_delete({'_id':ObjectId(id)})
        if res: temp = getData(res)
        else: temp = res
        return jsonify(temp)
    return make_response("No tiene permiso para realizar esta acción.", 403)

#-----------------------------------------------------------------------------------------------------------------
#FRONTEND ROUTES

@app.route('/api/index', methods=['GET'])
@jwt_required()
def getIndex():
    res = db.pedimentos.find({}, {'num_pedimento':True, 'material': True, 'fecha_venc':True, '_id': False})
    cat = db.catalogo.find({}, {'tipo':True, 'nom': True, 'num_registro': True, '_id': False})
    return jsonify(list(res), list(cat))

@app.route('/api/addFP', methods=['GET'])
@jwt_required()
def getAddFP():
    ped = db.pedimentos.find({}, {'num_pedimento': True, '_id': False})
    catalogo = db.catalogo.find({"tipo":"proveedor"}, {'nom': True, 'num_registro': True, '_id': False})
    return jsonify(list(ped), list(catalogo))

@app.route('/api/editFP/<num_registro>', methods=['GET'])
@jwt_required()
def getEditFP(num_registro):
    elem = db.catalogo.find_one({"num_registro": num_registro}, {'nom': True, 'num_registro': True, '_id': False})
    catalogo = db.catalogo.find({"tipo":"proveedor"}, {'nom': True, 'num_registro': True, '_id': False})
    return jsonify(elem, list(catalogo))

@app.route('/api/addFC', methods=['GET'])
@jwt_required()
def getAddFC():
    ped = db.pedimentos.find({}, {'num_pedimento': True, '_id': False})
    catalogo = db.catalogo.find({"tipo":"cliente"}, {'nom': True, 'num_registro': True, '_id': False})
    return jsonify(list(ped), list(catalogo))

@app.route('/api/editFC/<num_registro>', methods=['GET'])
@jwt_required()
def getEditFC(num_registro):
    elem = db.catalogo.find_one({"num_registro": num_registro}, {'nom': True, 'num_registro': True, '_id': False})
    catalogo = db.catalogo.find({"tipo":"cliente"}, {'nom': True, 'num_registro': True, '_id': False})
    return jsonify(elem, list(catalogo))

@app.route('/api/addPL', methods=['GET'])
@jwt_required()
def getAddPL():
    catalogo = db.catalogo.find({"tipo":"proveedor"}, {'nom': True, 'num_registro': True, '_id': False})
    return jsonify(list(catalogo))

@app.route('/api/editPL/<num_registro>', methods=['GET'])
@jwt_required()
def getEditPL(num_registro):
    elem = db.catalogo.find_one({"num_registro": num_registro}, {'nom': True, 'num_registro': True, '_id': False})
    catalogo = db.catalogo.find({"tipo":"proveedor"}, {'nom': True, 'num_registro': True, '_id': False})
    return jsonify(elem, list(catalogo))

#-----------------------------------------------------------------------------------------------------------------
#HELPERS

def getData(data):
    data['_id'] = str(data['_id'])
    if ('doc' in data): data['doc'] = str(data['doc'])
    if ('registro' in data): data['registro']['_id'] = str(data['registro']['_id'])
    if ('datos' in data): data['datos']['_id'] = str(data['datos']['_id'])
    if ('xml' in data): data['xml'] = str(data['xml'])
    if ('pdf' in data): data['pdf'] = str(data['pdf'])
    if ('img' in data): data['img'] = str(data['img'])
    return data

def setData(data):
    if ('doc' in data and "doc_filename" not in data and data['doc'] != 'None'): data['doc'] = ObjectId(data['doc'])
    if ('xml' in data and "xml_filename" not in data and data['xml'] != 'None'): data['xml'] = ObjectId(data['xml'])
    if ('pdf' in data and "pdf_filename" not in data and data['pdf'] != 'None'): data['pdf'] = ObjectId(data['pdf'])
    if ('img' in data and "img_filename" not in data and data['img'] != 'None'): data['img'] = ObjectId(data['img'])
    return data

def setFilename(file_id, filename):
    bucket.rename(file_id, filename)

def delFile(id):
    bucket.delete(ObjectId(id))

def putFile(file, args):
    return file_manager.put(file, **args)

def getFile(id):
    return bucket.find({'_id':ObjectId(id)})[0]

def getFilename(id):
    return db.fs.files.find({'_id':ObjectId(id)})[0]['filename']

def getMimeFile(filename):
    mime = guess_type(filename)[0]
    mime = 'text/plain' if mime == "text/xml" else mime
    return mime

def setMimeFile(id, filename):
    mime = getMimeFile(filename)
    db.fs.files.find_one_and_update({'_id':id}, {'$set': {"metadata": mime}})

def chkPermissions(usuario, seccion, op):
    res = db.usuarios.find_one({'user' : usuario})
    res['roles'] = loads(res['roles'].replace("'", '"'))
    if res:
        if op in res['roles'][seccion]: return True
    else: return False

def getReadPermissions(usuario):
    res = db.usuarios.find_one({'user' : usuario})
    res['roles'] = loads(res['roles'].replace("'", '"'))
    permisos = list()
    if res:
        for seccion in res['roles']:
            if 'r' in res['roles'][seccion]:
                permisos.append(seccion)
    return permisos