from base64 import b64encode
from datetime import datetime
from flask.helpers import make_response
from app import app, forbidden, sendRequest, convertirBytes
from flask import render_template, session, request, redirect, url_for
from app.api import *

@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@forbidden
def index():
    if request.method == 'POST':
        datos = {
            'fecha_inicio' : request.form['fecha_1_inicio'],
            'fecha_fin' : request.form['fecha_1_fin'],
            'fecha_enviado_inicio' : request.form['fecha_2_inicio'],
            'fecha_enviado_fin' : request.form['fecha_2_fin'],
            'fecha_venc' : request.form['fecha_venc'],
            'proveedor': request.form['p'],
            'cliente': request.form['c']
        }
        listado = sendRequest("post", "reporte/"+request.form['tipo'], session['token'], datos)
        reporte = { 'inicio': datos['fecha_inicio'], 'fin': datos['fecha_fin'] }

        if request.form['tipo'] == 'archivos':
            return render_template('archivos/archivos.html', titulo="Reporte de Archivos", archivos=listado, reporte=reporte, usuario=session['usuario'])
        if request.form['tipo'] == 'fp':
            return render_template('proveedores/proveedores.html', titulo="Reporte de Facturas de Proveedores", proveedores=listado, reporte=reporte, usuario=session['usuario'])
        if request.form['tipo'] == 'fc':
            return render_template('clientes/clientes.html', titulo="Reporte de Facturas de Clientes", clientes=listado, reporte=reporte, usuario=session['usuario'])
        if request.form['tipo'] == 'pedimentos':
            return render_template('pedimentos/pedimentos.html', titulo="Reporte de Pedimentos", pedimentos=listado, reporte=reporte, usuario=session['usuario'])
        if request.form['tipo'] == 'pl':
            reporte['inicio_2'] = datos['fecha_enviado_inicio']
            reporte['fin_2'] = datos['fecha_enviado_fin']
            return render_template('packinglists/packinglists.html', titulo="Reporte de Packing Lists", packinglists=listado, reporte=reporte, usuario=session['usuario'])
    else:
        if 'usuario' in session:
            if chkPermissions(session['usuario'], 'pedimentos', 'r'):
                pedimentos = sendRequest("get", "pedimentos", session['token'])
                _, cat = sendRequest("get", "index", session['token'])
                permiso = True
            else:
                pedimentos, cat = sendRequest("get", "index", session['token'])
                permiso = False
            fecha = datetime.now().strftime("%Y-%m-%d")
            
            temp = getReadPermissions(session['usuario'])
            docs = list()
            for i in temp:
                if i == 'fp': docs.append({ "db": i, "tipo": "Factura de Proveedores" })
                if i == 'fc': docs.append({ "db": i, "tipo": "Factura de Clientes" })
                if i == 'pedimentos': docs.append({ "db": i, "tipo": "Pedimentos" })
                if i == 'pl': docs.append({ "db": i, "tipo": "Packing Lists" })
                if i == 'archivos': docs.append({ "db": i, "tipo": "Archivos" })

            return render_template('index.html', titulo="Index", docs=docs, permiso=permiso, pedimentos=pedimentos, catalogo=cat, fecha=fecha, usuario=session['usuario'])
        return redirect(url_for('login'))

#---------------------------------------------------------------------------------------------------------------------------------
#FACTURAS DE PROVEEDORES

@app.route('/proveedores')
@forbidden
def proveedores():
    if 'usuario' in session:
        select = sendRequest("get", "proveedores", session['token'])
        return render_template('proveedores/proveedores.html', proveedores=select, titulo="Facturas de Proveedores", usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/addFP', methods=['POST', 'GET'])
@forbidden
def addFP():
    if request.method == 'POST':
        datos = {
            'num_factura' : request.form['num_factura'],
            'fecha_factura' : request.form['fecha_factura'],
            'num_registro' : request.form['num_registro'],
            'num_pedimento' : request.form['num_pedimento'],
            'fecha_venc' : request.form['fecha_venc'],
            'xml': b64encode(request.files['xml'].read()) if request.files['xml'].filename != '' else None,
            'xml_filename': request.files['xml'].filename,
            'pdf': b64encode(request.files['pdf'].read()) if request.files['pdf'].filename != '' else None,
            'pdf_filename': request.files['pdf'].filename
        }
        
        if sendRequest("get", "proveedores?num_factura=" + datos['num_factura'], session['token']):
            ped, catalogo = sendRequest("get", "addFP", session['token'])
            return render_template('proveedores/addFP.html', registros=catalogo, disp=True, pedimentos=ped, titulo="Facturas de Proveedores", usuario=session['usuario'])
        else:
            sendRequest("post", "proveedores", session['token'], datos)
        return redirect(url_for('proveedores'))
    else:
        if 'usuario' in session:
            ped, catalogo = sendRequest("get", "addFP", session['token'])
            return render_template('proveedores/addFP.html', registros=catalogo, pedimentos=ped, titulo="Facturas de Proveedores", usuario=session['usuario'])
        return redirect(url_for('login'))

@app.route('/editFP', methods=['POST', 'GET'])
@forbidden
def editFP():
    id = request.args.get('id')
    if request.method == 'POST':
        datos = {
            'num_factura' : request.form['num_factura'],
            'fecha_factura' : request.form['fecha_factura'],
            'num_registro' : request.form['num_registro'],
            'num_pedimento' : request.form['num_pedimento'],
            'fecha_venc' : request.form['fecha_venc']
        }
        
        if (sendRequest("get", "proveedores/"+id, session['token'])[0]['num_factura'] != datos['num_factura']
            and sendRequest("get", "proveedores?num_factura="+datos['num_factura'], session['token'])):
            elem = sendRequest("get", "proveedores", session['token'])[0]
            if elem['xml'] != None:
                xml = getFile(id=elem['xml'])
                elem['xml_file'] = xml.filename
            if elem['pdf'] != None:
                pdf = getFile(id=elem['pdf'])
                elem['pdf_file'] = pdf.filename
            cat, select = sendRequest("get", "editFP/"+elem['num_registro'], session['token'])
            elem['nom'] = cat['nom']
            return render_template('proveedores/editFP.html', disp=True, i=elem, registros=select, titulo="Facturas de Proveedores", usuario=session['usuario'])       
        else: 
            if (request.form['doc'] == 'No'):
                elem = sendRequest("get", "proveedores/"+id, session['token'])[0]
                if (elem['xml'] != 'None'): delFile(elem['xml'])
                if (elem['pdf'] != 'None'): delFile(elem['pdf'])
                sendRequest("put", "proveedores/"+id, session['token'], { 'xml' : None, 'pdf' : None })
                
            elif (request.form['doc'] == 'Si'):
                if (request.files['xml'].filename != ""):
                    #Insert new XML
                    xml_args = {}
                    xml_args["filename"] = request.files['xml'].filename
                    xml_args["metadata"] = "text/plain"
                    datos['xml'] = putFile(request.files['xml'], xml_args)

                    #Get old XML
                    elem = sendRequest("get", "proveedores/"+id, session['token'])[0]

                    #Delete old XML
                    if (elem['xml'] != 'None'): delFile(elem['xml'])

                if (request.files['pdf'].filename != ""):
                    #Insert new PDF
                    pdf_args = {}
                    pdf_args["filename"] = request.files['pdf'].filename
                    pdf_args["metadata"] = "application/pdf"
                    datos['pdf'] = putFile(request.files['pdf'], pdf_args)
                    
                    #Get old XML
                    elem = sendRequest("get", "proveedores/"+id, session['token'])[0]

                    #Delete old PDF
                    if (elem['pdf'] != 'None'): delFile(elem['pdf'])
            sendRequest("put", "proveedores/"+id, session['token'], datos)
        return redirect(url_for('proveedores', id=id))
    else:
        if 'usuario' in session:
            elem = sendRequest("get", "proveedores/"+id, session['token'])[0]
            if elem['xml'] != 'None':
                xml = getFile(id=elem['xml'])
                elem['xml_file'] = xml.filename
            if elem['pdf'] != 'None':
                pdf = getFile(id=elem['pdf'])
                elem['pdf_file'] = pdf.filename
            
            cat, select = sendRequest("get", "editFP/"+elem['num_registro'], session['token'])
            elem['nom'] = cat['nom']
            return render_template('proveedores/editFP.html', i=elem, registros=select, titulo="Facturas de Proveedores", usuario=session['usuario'])
        return redirect(url_for('login'))

@app.route('/deleteFP')
@forbidden
def deleteFP():
    if 'usuario' in session:
        id = request.args.get('id')
        sendRequest("delete", "proveedores/"+id, session['token'])
        return redirect(url_for('proveedores'))
    return redirect(url_for('login'))

#---------------------------------------------------------------------------------------------------------------------------------
#FACTURAS DE CLIENTES

@app.route('/clientes')
@forbidden
def clientes():
    if 'usuario' in session:
        select = sendRequest("get", "clientes", session['token'])
        return render_template('clientes/clientes.html', clientes=select, titulo="Facturas de Clientes", usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/addFC', methods=['POST', 'GET'])
@forbidden
def addFC():
    if request.method == 'POST':
        datos = {
            'num_factura' : request.form['num_factura'],
            'fecha_factura' : request.form['fecha_factura'],
            'num_registro' : request.form['num_registro'],
            'num_pedimento' : request.form['num_pedimento'],
            'xml': b64encode(request.files['xml'].read()) if request.files['xml'].filename != '' else None,
            'xml_filename': request.files['xml'].filename,
            'pdf': b64encode(request.files['pdf'].read()) if request.files['pdf'].filename != '' else None,
            'pdf_filename': request.files['pdf'].filename
        }

        if (sendRequest("get", "clientes?num_factura=" + datos['num_factura'], session['token'])):
            ped, catalogo = sendRequest("get", "addFC", session['token'])
            return render_template('clientes/addFC.html', registros=catalogo, disp=True, pedimentos=ped, titulo="Facturas de Clientes", usuario=session['usuario'])
        else:
            sendRequest("post", "clientes", session['token'], datos)
        return redirect(url_for('clientes'))
    else:
        if 'usuario' in session:
            ped, catalogo = sendRequest("get", "addFC", session['token'])
            return render_template('clientes/addFC.html', registros=catalogo, pedimentos=ped, titulo="Facturas de Clientes", usuario=session['usuario'])
        return redirect(url_for('login'))

@app.route('/editFC', methods=['POST', 'GET'])
@forbidden
def editFC():
    id = request.args.get('id')
    if request.method == 'POST':
        datos = {
            'num_factura' : request.form['num_factura'],
            'fecha_factura' : request.form['fecha_factura'],
            'num_registro' : request.form['num_registro'],
            'num_pedimento' : request.form['num_pedimento']
        }
        
        if (sendRequest("get", "clientes/"+id, session['token'])[0]['num_factura'] != datos['num_factura']
            and sendRequest("get", "clientes?num_factura"+datos['num_factura'], session['token'])):
            elem = sendRequest("get", "clientes", session['token'])[0]
            if elem['xml'] != None:
                xml = getFile(id=elem['xml'])
                elem['xml_file'] = xml.filename
            if elem['pdf'] != None:
                pdf = getFile(id=elem['pdf'])
                elem['pdf_file'] = pdf.filename
            cat, select = sendRequest("get", "editFC/"+elem['num_registro'], session['token'])
            elem['nom'] = cat['nom']
            return render_template('clientes/editFC.html', disp=True, i=elem, registros=select, titulo="Facturas de Clientes", usuario=session['usuario'])       
        else: 
           
            if (request.form['doc'] == 'No'):
                elem = sendRequest("get", "clientes/"+id, session['token'])[0]
                if (elem['xml'] != 'None'): delFile(elem['xml'])
                if (elem['pdf'] != 'None'): delFile(elem['pdf'])
                sendRequest("put", "clientes/"+id, session['token'], { 'xml' : None, 'pdf' : None })
                
            elif (request.form['doc'] == 'Si'):
                if (request.files['xml'].filename != ""):
                    #Insert new XML
                    xml_args = {}
                    xml_args["filename"] = request.files['xml'].filename
                    xml_args["metadata"] = "text/plain"
                    datos['xml'] = putFile(request.files['xml'], xml_args)

                    #Get old XML
                    elem = sendRequest("get", "clientes/"+id, session['token'])[0]

                    #Delete old XML
                    if (elem['xml'] != 'None'): delFile(elem['xml'])

                if (request.files['pdf'].filename != ""):
                    #Insert new PDF
                    pdf_args = {}
                    pdf_args["filename"] = request.files['pdf'].filename
                    pdf_args["metadata"] = "application/pdf"
                    datos['pdf'] = putFile(request.files['pdf'], pdf_args)
                    
                    #Get old XML
                    elem = sendRequest("get", "clientes/"+id, session['token'])[0]

                    #Delete old PDF
                    if (elem['pdf'] != 'None'): delFile(elem['pdf'])
            
            sendRequest("put", "clientes/"+id, session['token'], datos)
        return redirect(url_for('clientes', id=id))
    else:
        if 'usuario' in session:
            elem = sendRequest("get", "clientes/"+id, session['token'])[0]
            if elem['xml'] != 'None':
                xml = getFile(id=elem['xml'])
                elem['xml_file'] = xml.filename
            if elem['pdf'] != 'None':
                pdf = getFile(id=elem['pdf'])
                elem['pdf_file'] = pdf.filename
            
            cat, select = sendRequest("get", "editFC/"+elem['num_registro'], session['token'])
            elem['nom'] = cat['nom']
            return render_template('clientes/editFC.html', i=elem, registros=select, titulo="Facturas de Clientes", usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/deleteFC')
@forbidden
def deleteFC():
    if 'usuario' in session:
        id = request.args.get('id')
        sendRequest("delete", "clientes/"+id, session['token'])
        return redirect(url_for('clientes'))
    return redirect(url_for('login'))

#---------------------------------------------------------------------------------------------------------------------------------
#CATALOGO

@app.route('/catalogo')
@forbidden
def catalogo():
    if 'usuario' in session:
        select = sendRequest("get", "catalogo", session['token'])
        return render_template('catalogo/catalogo.html', registros=select, titulo="Catálogo", usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/addC', methods=['POST', 'GET'])
@forbidden
def addC():
    if request.method == 'POST':
        datos = {
            'tipo' : request.form['tipo'],
            'num_registro' : request.form['num_registro'],
            'nom' : request.form['nom'],
            'dir': request.form['dir'],
            'tel': request.form['tel'],
            'rfc': request.form['rfc'],
            'correo': request.form['correo']
        }
        
        if sendRequest("get", "catalogo?num_registro=" + datos['num_registro'], session['token']):
            return render_template('catalogo/addC.html', disp=True, href="/catalogo", reg_texto="Catálogo", titulo="Catálogo", usuario=session['usuario'])
        else: sendRequest("post", "catalogo", session['token'], datos)
        return redirect(url_for('catalogo'))
    else:
        if 'usuario' in session:
            return render_template('catalogo/addC.html', href="/catalogo", reg_texto="Catálogo", titulo="Catálogo", usuario=session['usuario'])
        return redirect(url_for('login'))

@app.route('/addCC', methods=['POST', 'GET'])
@forbidden
def addCC():
    if request.method == 'POST':
        datos = {
            'tipo' : request.form['tipo'],
            'num_registro' : request.form['num_registro'],
            'nom' : request.form['nom'],
            'dir': request.form['dir'],
            'tel': request.form['tel'],
            'rfc': request.form['rfc'],
            'correo': request.form['correo']
        }
        
        if sendRequest("get", "catalogo?num_registro=" + datos['num_registro'], session['token']):
            ruta = '/' + request.referrer.rsplit('/', 1)[-1]
            return render_template('catalogo/addC.html', disp=True, href=ruta, reg_texto="Factura de Clientes", titulo="Catálogo", sel="cliente", usuario=session['usuario'])
        else: sendRequest("post", "catalogo", session['token'], datos)
        return redirect(url_for('addFC'))
    else:
        if 'usuario' in session:
            ruta = '/' + request.referrer.rsplit('/', 1)[-1]
            return render_template('catalogo/addC.html', href=ruta, reg_texto="Factura de Clientes", titulo="Catálogo", sel="cliente", usuario=session['usuario'])
        return redirect(url_for('login'))

@app.route('/addCP', methods=['POST', 'GET'])
@forbidden
def addCP():
    if request.method == 'POST':
        datos = {
            'tipo' : request.form['tipo'],
            'num_registro' : request.form['num_registro'],
            'nom' : request.form['nom'],
            'dir': request.form['dir'],
            'tel': request.form['tel'],
            'rfc': request.form['rfc'],
            'correo': request.form['correo']
        }
        
        if sendRequest("get", "catalogo?num_registro=" + datos['num_registro'], session['token']):
            ruta = '/' + request.referrer.rsplit('/', 1)[-1]
            return render_template('catalogo/addC.html', disp=True, href=ruta, reg_texto="Factura de Proveedores", titulo="Catálogo", sel="proveedor", usuario=session['usuario'])
        else: sendRequest("post", "catalogo", session['token'], datos)
        return redirect(url_for('addFP'))
    else:
        if 'usuario' in session:
            ruta = '/' + request.referrer.rsplit('/', 1)[-1]
            return render_template('catalogo/addC.html', href=ruta, reg_texto="Factura de Proveedores", titulo="Catálogo", sel="proveedor", usuario=session['usuario'])
        return redirect(url_for('login'))

@app.route('/editC', methods=['POST', 'GET'])
@forbidden
def editC():
    id = request.args.get('id')
    if request.method == 'POST':
        datos = {
            'tipo' : request.form['tipo'],
            'num_registro' : request.form['num_registro'],
            'nom' : request.form['nom'],
            'dir' : request.form['dir'],
            'tel' : request.form['tel'],
            'rfc' : request.form['rfc'],
            'correo': request.form['correo']
        }

        if (sendRequest("get", "catalogo/"+id, session['token'])[0]['num_registro'] != datos['num_registro']
            and sendRequest("get", "catalogo?num_registro=" + datos['num_registro'], session['token'])):
            elem = sendRequest("get", "catalogo/"+id, session['token'])[0]
            return render_template('catalogo/editC.html', disp=True, i=elem, titulo="Catálogo", usuario=session['usuario'])      
        else: sendRequest("put", "catalogo/"+id, session['token'], datos)
        
        return redirect(url_for('catalogo'))
    else:
        if 'usuario' in session:
            elem = sendRequest("get", "catalogo/"+id, session['token'])[0]
            return render_template('catalogo/editC.html', i=elem, titulo="Catálogo", usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/deleteC')
@forbidden
def deleteC():
    if 'usuario' in session:
        id = request.args.get('id')
        sendRequest("delete", "catalogo/"+id, session['token'])
        return redirect(url_for('catalogo'))
    return redirect(url_for('login'))


#---------------------------------------------------------------------------------------------------------------------------------
#PEDIMENTOS

@app.route('/pedimentos')
@forbidden
def pedimentos():
    if 'usuario' in session:
        select = sendRequest("get", "pedimentos", session['token'])
        return render_template('pedimentos/pedimentos.html', pedimentos=select, titulo="Pedimentos", usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/addPed', methods=['POST', 'GET'])
@forbidden
def addPed():
    if request.method == 'POST':
        datos = {
            'num_pedimento' : request.form['num_pedimento'],
            'fecha_pedimento' : request.form['fecha_pedimento'],
            'fecha_venc' : request.form['fecha_venc'],
            'material': request.form['material'],
            'aduana': request.form['aduana'],
            'exportador': request.form['exportador'],
            'doc': b64encode(request.files['doc'].read()) if request.files['doc'].filename != '' else None,
            'doc_filename': request.files['doc'].filename
        }
        
        if sendRequest("get", "pedimentos?num_pedimento="+ datos['num_pedimento'], session['token']):
            return render_template('pedimentos/addPed.html', disp=True, titulo="Pedimentos", usuario=session['usuario'])
        else: sendRequest("post", "pedimentos", session['token'], datos)
        return redirect(url_for('pedimentos'))
    else:
        if 'usuario' in session:
            return render_template('pedimentos/addPed.html', titulo="Pedimentos", usuario=session['usuario'])
        return redirect(url_for('login'))

@app.route('/editPed', methods=['POST', 'GET'])
@forbidden
def editPed():
    id = request.args.get('id')
    if request.method == 'POST':
        datos = {
            'num_pedimento' : request.form['num_pedimento'],
            'fecha_pedimento' : request.form['fecha_pedimento'],
            'fecha_venc' : request.form['fecha_venc'],
            'material' : request.form['material'],
            'aduana' : request.form['aduana'],
            'exportador' : request.form['exportador']
        }
        if (sendRequest("get", "pedimentos/"+id, session['token'])[0]['num_pedimento'] != datos['num_pedimento'] 
            and sendRequest("get", "pedimentos?num_pedimento="+datos['num_pedimento'], session['token'])):
            elem = sendRequest("get", "pedimentos/"+id, session['token'])[0]
            if elem['doc'] != 'None':
                doc = getFile(elem['doc'])
                elem['doc_file'] = doc.filename
            return render_template('pedimentos/editPed.html', disp=True, i=elem, titulo="Pedimentos", usuario=session['usuario'])       
        else:
            if (request.form['doc'] == 'No'):
                elem = sendRequest("get", "pedimentos/"+id, session['token'])[0]
                if (elem['doc'] != 'None'): delFile(elem['doc'])
                sendRequest("put", "pedimentos/"+id, session['token'], { 'doc': None })

            elif (request.form['doc'] == 'Si'):
                if (request.files['documento'].filename != ""):
                    #Insert new Doc
                    args = {}
                    args["filename"] = request.files['documento'].filename
                    args["metadata"] = getMimeFile(request.files['documento'].filename)
                    datos['doc'] = putFile(request.files['documento'], args)
                    
                    #Get old Doc
                    elem = sendRequest("get", "pedimentos/"+id, session['token'])[0]
                    #Delete old Doc
                    if (elem['doc'] != 'None'): delFile(elem['doc'])
            
            sendRequest("put", "pedimentos/"+id, session['token'], datos)

        return redirect(url_for('pedimentos'))
    else:
        if 'usuario' in session:
            elem = sendRequest("get", "pedimentos/"+id, session['token'])[0]
            if elem['doc'] != 'None':
                doc = getFile(elem['doc'])
                elem['doc_file'] = doc.filename
            return render_template('pedimentos/editPed.html', i=elem, titulo="Pedimentos", usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/deletePed')
@forbidden
def deletePed():
    if 'usuario' in session:
        id = request.args.get('id')
        sendRequest("delete", "pedimentos/"+id, session['token'])
        return redirect(url_for('pedimentos'))
    return redirect(url_for('login'))

#---------------------------------------------------------------------------------------------------------------------------------
#PACKING LISTS

@app.route('/packinglists')
@forbidden
def packinglists():
    if 'usuario' in session:
        select = sendRequest("get", "packinglists", session['token'])
        return render_template('packinglists/packinglists.html', packinglists=select, titulo="Packing Lists", usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/addPL', methods=['POST', 'GET'])
@forbidden
def addPL():
    if request.method == 'POST':
        datos = {
            'num_ref': request.form['num_ref'],
            'num_registro': request.form['num_registro'],
            'fecha_recibido': request.form['fecha_recibido'],
            'fecha_enviado': request.form['fecha_enviado'],
            'doc': b64encode(request.files['doc'].read()) if request.files['doc'].filename != '' else None,
            'doc_filename': request.files['doc'].filename,
            'img': b64encode(request.files['img'].read()) if request.files['img'].filename != '' else None,
            'img_filename': request.files['img'].filename
        }

        if (sendRequest("get", "packinglists?num_ref=" + datos['num_ref'], session['token'])):
            catalogo = sendRequest("get", "addPL", session['token'])
            return render_template('packinglists/addPL.html', registros=catalogo, disp=True, titulo="Packing Lists", usuario=session['usuario'])
        else: sendRequest("post", "packinglists", session['token'], datos)
        return redirect(url_for('packinglists'))
    else:
        if 'usuario' in session:
            catalogo = sendRequest("get", "addPL", session['token'])
            return render_template('packinglists/addPL.html', registros=catalogo, titulo="Packing Lists", usuario=session['usuario'])
        return redirect(url_for('login'))

@app.route('/editPL', methods=['POST', 'GET'])
@forbidden
def editPL():
    id = request.args.get('id')
    if request.method == 'POST':
        datos = {
            'num_ref' : request.form['num_ref'],
            'num_registro' : request.form['num_registro'],
            'fecha_recibido' : request.form['fecha_recibido'],
            'fecha_enviado' : request.form['fecha_enviado']
        }
        
        if (sendRequest("get", "packinglists/"+id, session['token'])[0]['num_ref'] != datos['num_ref']
            and sendRequest("get", "packinglists?num_ref"+datos['num_ref'], session['token'])):
            elem = sendRequest("get", "packinglists", session['token'])[0]
            if elem['doc'] != None:
                doc = getFile(id=elem['doc'])
                elem['doc_file'] = doc.filename
            if elem['img'] != None:
                img = getFile(id=elem['img'])
                elem['img_file'] = img.filename
            cat, select = sendRequest("get", "editPL/"+elem['num_registro'], session['token'])
            elem['nom'] = cat['nom']
            return render_template('packinglists/editPL.html', disp=True, i=elem, registros=select, titulo="Packing Lists", usuario=session['usuario'])       
        else: 
            if (request.form['doc'] == 'No'):
                elem = sendRequest("get", "packinglists/"+id, session['token'])[0]
                if (elem['doc'] != 'None'): delFile(elem['doc'])
                sendRequest("put", "packinglists/"+id, session['token'], { 'doc': None })
                 
            elif (request.form['doc'] == 'Si'):
                if (request.files['documento'].filename != ""):
                    #Insert new Doc
                    args = {}
                    args["filename"] = request.files['documento'].filename
                    args["metadata"] = getMimeFile(request.files['documento'].filename)
                    datos['doc'] = putFile(request.files['documento'], args)   
                    #Get old Doc
                    elem = sendRequest("get", "packinglists/"+id, session['token'])[0]
                    #Delete old Doc
                    if (elem['doc'] != 'None'): delFile(elem['doc'])

            if (request.form['img'] == 'No'):
                elem = sendRequest("get", "packinglists/"+id, session['token'])[0]
                if (elem['img'] != 'None'): delFile(elem['img'])
                sendRequest("put", "packinglists/"+id, session['token'], { 'img': None })
                 
            elif (request.form['img'] == 'Si'):
                if (request.files['imagen'].filename != ""):
                    #Insert new Img
                    args = {}
                    args["filename"] = request.files['imagen'].filename
                    args["metadata"] = getMimeFile(request.files['imagen'].filename)
                    datos['img'] = putFile(request.files['imagen'], args)
                    #Get old Img
                    elem = sendRequest("get", "packinglists/"+id, session['token'])[0]
                    #Delete old Img
                    if (elem['img'] != 'None'): delFile(elem['img'])
            
            sendRequest("put", "packinglists/"+id, session['token'], datos)

        return redirect(url_for('packinglists'))
    else:
        if 'usuario' in session:
            elem = sendRequest("get", "packinglists/"+id, session['token'])[0]
            if elem['doc'] != 'None':
                doc = getFile(id=elem['doc'])
                elem['doc_file'] = doc.filename
            if elem['img'] != 'None':
                img = getFile(id=elem['img'])
                elem['img_file'] = img.filename
            
            cat, select = sendRequest("get", "editPL/"+elem['num_registro'], session['token'])
            elem['nom'] = cat['nom']
            return render_template('packinglists/editPL.html', i=elem, registros=select, titulo="Packing Lists", usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/deletePL')
@forbidden
def deletePL():
    if 'usuario' in session:
        id = request.args.get('id')
        sendRequest("delete", "packinglists/"+id, session['token'])
        return redirect(url_for('packinglists'))
    return redirect(url_for('login'))


#---------------------------------------------------------------------------------------------------------------------------------
#ARCHIVOS

@app.route('/archivos')
@forbidden
def archivos():
    if 'usuario' in session:
        select = sendRequest("get", "archivos", session['token'])
        for i in select: i['datos']['length'] = convertirBytes(i['datos']['length'])
        return render_template('archivos/archivos.html', archivos=select, titulo="Archivos", usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/addArchivo', methods=['POST', 'GET'])
@forbidden
def addArchivo():
    if request.method == 'POST':
        datos = {
            'num_ref': request.form['num_ref'],
            'fecha': request.form['fecha'],
            'desc': request.form['desc'],
            'doc': b64encode(request.files['doc'].read()) if request.files['doc'].filename != '' else None,
            'doc_filename': request.files['doc'].filename
        }
        
        if sendRequest("get", "archivos?num_ref="+datos['num_ref'], session['token']):
            return render_template('archivos/addArchivo.html', disp=True, titulo="Archivos", usuario=session['usuario'])
        else: sendRequest("post", "archivos", session['token'], datos)
        return redirect(url_for('archivos'))
    else:
        if 'usuario' in session:
            return render_template('archivos/addArchivo.html', titulo="Archivos", usuario=session['usuario'])
        return redirect(url_for('login'))

@app.route('/editArchivo', methods=['POST', 'GET'])
@forbidden
def editArchivo():
    id = request.args.get('id')
    if request.method == 'POST':
        datos = {
            'num_ref' : request.form['num_ref'],
            'fecha' : request.form['fecha'],
            'desc' : request.form['desc']
        }
        if (sendRequest("get", "archivos/"+id, session['token'])[0]['num_ref'] != datos['num_ref'] 
            and sendRequest("get", "archivos?num_ref="+datos['num_ref'], session['token'])):
            elem = sendRequest("get", "archivos/"+id, session['token'])[0]
            if elem['doc'] != 'None':
                doc = getFile(elem['doc'])
                elem['doc_file'] = doc.filename
            return render_template('archivos/editArchivo.html', disp=True, i=elem, titulo="Archivos", usuario=session['usuario'])       
        else:
            if (request.files['documento'].filename != ""):
                #Insert new Doc
                args = {}
                args["filename"] = request.files['documento'].filename
                args["metadata"] = getMimeFile(request.files['documento'].filename)
                datos['doc'] = putFile(request.files['documento'], args)
                
                #Get old Doc
                elem = sendRequest("get", "archivos/"+id, session['token'])[0]
                #Delete old Doc
                if (elem['doc'] != 'None'): delFile(elem['doc'])
            
            sendRequest("put", "archivos/"+id, session['token'], datos)

        return redirect(url_for('archivos'))
    else:
        if 'usuario' in session:
            elem = sendRequest("get", "archivos/"+id, session['token'])[0]
            if elem['doc'] != 'None':
                doc = getFile(elem['doc'])
                elem['doc_file'] = doc.filename
            return render_template('archivos/editArchivo.html', i=elem, titulo="Archivos", usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/deleteArchivo')
@forbidden
def deleteArchivo():
    if 'usuario' in session:
        id = request.args.get('id')
        sendRequest("delete", "archivos/"+id, session['token'])
        return redirect(url_for('archivos'))
    return redirect(url_for('login'))

#---------------------------------------------------------------------------------------------------------------------------------
#USUARIOS

@app.route('/usuarios')
@forbidden
def usuarios():
    if 'usuario' in session:
        select = sendRequest("get", "usuarios", session['token'])
        return render_template('usuarios/usuarios.html', usuarios=select, titulo="Usuarios", usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/addUsuario', methods=['POST', 'GET'])
@forbidden
def addUsuario():
    if request.method == 'POST':
        datos = {
            'asignacion': request.form['asignacion'],
            'user': request.form['user'],
            'password': request.form['password']
        }

        permisos = { key: request.form[key] for key in request.form.keys() if key not in ['asignacion', 'user', 'password'] }
        tags = [('fp', 'fp'), ('fc', 'fc'), ('p', 'pedimentos'), ('pl', 'pl'), ('c', 'catalogo'), ('a', 'archivos'), ('u', 'usuarios')]
        roles = dict.fromkeys(['fp', 'fc', 'pedimentos', 'pl', 'catalogo', 'archivos', 'usuarios'])
        for tag, db in tags:
            rol = str()
            if (tag+'_c' in permisos): rol+='c'
            if ((tag+'_r' or tag+'_u' or tag+'_d') in permisos): rol+='r'
            if (tag+'_u' in permisos): rol+='u'
            if (tag+'_d' in permisos): rol+='d'
            roles[db]= rol
        
        datos['roles'] = roles

        if sendRequest("get", "usuarios?user="+datos['user'], session['token']):
            return render_template('usuarios/addUsuario.html', disp=True, titulo="Usuarios", usuario=session['usuario'])
        else: sendRequest("post", "usuarios", session['token'], datos)

        return redirect(url_for('usuarios'))
    else:
        if 'usuario' in session:
            return render_template('usuarios/addUsuario.html', titulo="Usuarios", usuario=session['usuario'])
        return redirect(url_for('login'))

@app.route('/editUsuario', methods=['POST', 'GET'])
@forbidden
def editUsuario():
    id = request.args.get('id')
    if request.method == 'POST':
        datos = {
            'asignacion' : request.form['asignacion'],
            'user' : request.form['user'],
            'password' : request.form['password']
        }

        permisos = { key: request.form[key] for key in request.form.keys() if key not in ['asignacion', 'user', 'password'] }
        tags = [('fp', 'fp'), ('fc', 'fc'), ('p', 'pedimentos'), ('pl', 'pl'), ('c', 'catalogo'), ('a', 'archivos'), ('u', 'usuarios')]
        roles = dict.fromkeys(['fp', 'fc', 'pedimentos', 'pl', 'catalogo', 'archivos', 'usuarios'])

        for tag, db in tags:
            rol = str()
            if (tag+'_c' in permisos): rol+='c'
            if ((tag+'_r' or tag+'_u' or tag+'_d') in permisos): rol+='r'
            if (tag+'_u' in permisos): rol+='u'
            if (tag+'_d' in permisos): rol+='d'
            roles[db]= rol
        
        datos['roles'] = str(roles)

        if (sendRequest("get", "usuarios/"+id, session['token'])[0]['user'] != datos['user'] 
            and sendRequest("get", "usuarios?user="+datos['user'], session['token'])):
            elem = sendRequest("get", "usuarios/"+id, session['token'])[0]
            return render_template('archivos/editArchivo.html', disp=True, i=elem, titulo="Usuarios", usuario=session['usuario'])       
        else:           
            sendRequest("put", "usuarios/"+id, session['token'], datos)

        return redirect(url_for('usuarios'))
    else:
        if 'usuario' in session:
            elem = sendRequest("get", "usuarios/"+id, session['token'])[0]
            
            roles = dict.fromkeys(['fp_c', 'fp_r', 'fp_u', 'fp_d',
                                    'fc_c', 'fc_r', 'fc_u', 'fc_d',
                                    'p_c', 'p_r', 'p_u', 'p_d',
                                    'pl_c', 'pl_r', 'pl_u', 'pl_d',
                                    'c_c', 'c_r', 'c_u', 'c_d',
                                    'a_c', 'a_r', 'a_u', 'a_d',
                                    'u_c', 'u_r', 'u_u', 'u_d'])

            elem['roles'] = loads(elem['roles'].replace("'", '"'))
            tags = [('fp', 'fp'), ('fc', 'fc'), ('p', 'pedimentos'), ('pl', 'pl'), ('c', 'catalogo'), ('a', 'archivos'), ('u', 'usuarios')]
            for new_key, old_key in tags: elem['roles'][new_key] = elem['roles'].pop(old_key)
            for key, val in elem['roles'].items():
                if 'c' in val: roles[key+"_c"] = True
                if 'r' in val: roles[key+"_r"] = True
                if 'u' in val: roles[key+"_u"] = True
                if 'd' in val: roles[key+"_d"] = True
            elem['roles'] = roles
            return render_template('usuarios/editUsuario.html', i=elem, titulo="Usuarios", usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/deleteUsuario')
@forbidden
def deleteUsuario():
    if 'usuario' in session:
        id = request.args.get('id')
        sendRequest("delete", "usuarios/"+id, session['token'])
        return redirect(url_for('usuarios'))
    return redirect(url_for('login'))


#---------------------------------------------------------------------------------------------------------------------------------
#HELPERS

@app.route('/file/<id>')
def file(id):
    doc = getFile(id)
    res = make_response(doc.read())
    res.mimetype = doc.metadata
    res.headers.add_header('Content-Disposition', 'filename='+doc.filename)
    return res

@app.route('/verDoc/<tipo>')
def verDoc(tipo):
    if 'usuario' in session:
        id = request.args.get('id')
        if tipo == "fp":
            factura = sendRequest("get", "proveedores?xml="+id, session['token'])
            if factura == None:
                factura = sendRequest("get", "proveedores?pdf="+id, session['token'])
            t = "Facturas de proveedores"
            l = "/proveedores?id="+str(factura[0]['_id'])
        if tipo == "fc":
            factura = sendRequest("get", "clientes?xml="+id, session['token'])
            if factura == None:
                factura = sendRequest("get", "clientes?pdf="+id, session['token'])
            t = "Facturas de clientes"
            l = "/clientes?id="+str(factura[0]['_id'])
        if tipo == "p":
            ped = sendRequest("get", "pedimentos?doc="+id, session['token'])
            t = "Pedimentos"
            l = "/pedimentos?id="+str(ped[0]['_id'])
        if tipo == "pl":
            documento = sendRequest("get", "packinglists?doc="+id, session['token'])
            if documento == None:
                documento = sendRequest("get", "packinglists?img="+id, session['token'])
            t = "Packing Lists"
            l = "/packinglists?id="+str(documento[0]['_id'])
        if tipo == "a":
            archivo = sendRequest("get", "archivos?doc="+id, session['token'])
            t = "Archivos"
            l = "/archivos?id="+str(archivo[0]['_id'])

        filename = getFilename(id)
        return render_template('verDocumento.html', titulo=t, link=l, id=id, file=filename, usuario=session['usuario'])
    return redirect(url_for('login'))

from flask import send_file

@app.route('/descargar/<id>')
def descargar(id):
    doc = getFile(id)
    if doc.filename[-3] == 'xml': doc.metadata = "text/xml"
    return send_file(doc, mimetype=doc.metadata, as_attachment=True, download_name=doc.filename)

#---------------------------------------------------------------------------------------------------------------------------------
#LOGIN

@app.route('/login', methods=['POST', 'GET'])
def login():
    expired = request.args.get('expired')
    if request.method == 'POST':
        data = { "user" : request.form['usuario'], "password" : request.form['password'] }
        login_usuario = sendRequest("post", "login", data=data)
        if login_usuario == 422: return render_template('login.html', titulo="Login", disp=True)
        session['token'] = login_usuario
        session['usuario'] = request.form['usuario']
        return redirect(url_for('index'))
    else:
        if expired: return render_template('login.html', titulo="Login", disp=True, expired=True)
        return render_template('login.html', titulo="Login", disp=False)

@app.route('/logout')
def logout():
    if 'token' in session:
        session.pop('token')
        session.pop('usuario')
        return redirect(url_for('index'))

