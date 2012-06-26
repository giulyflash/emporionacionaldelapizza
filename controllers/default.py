# -*- coding: utf-8 -*-

# Emporio Nacional de la Pizza es una interfaz web de hexa662
# para gestión de pedidos online y envíos para pizzerías.

# Esta es una aplicación para demostración de la interfaz.
# Para implementaciones específicas y modificaciones puede
# puede comunicarse por medio del siguiente formulario de
# contacto:

# http://sites.google.com/site/hexa662/contacto-comercial

# Emporio Nacional de la Pizza - interfaz web para gestión de
# pedidos online y envíos para pizzerías
# Copyright (C) 2012  Alan Etkin <spametki@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Developed with web2py.

import datetime, random


#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    if not session.has_key('bienvenidos'):
        response.flash = T('Emporio Nacional de la Pizza v0.1a')
        session.bienvenidos = True

    if not control_acceso(session):
        raise HTTP(503,"Se alcanzó límite de consultas")
    else:
        return dict(message=T('Hello World'))
    
    
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()


def envio():

    if not control_acceso(session):
        raise HTTP(503,"Se alcanzó límite de consultas")


    # recuperar orden
    laorden = db(db.orden.id == int(request.args[0])).select().first()
    elcliente = db(db.cliente.id == laorden.cliente).select().first()
    
    id_cadetes = []
    # crear lista con id de cadete
    loscadetes = db(db.cadete).select()
    for cadete in loscadetes:
        id_cadetes.append(cadete.id)
        
    # seleccionar un cadete con random.choice
    cadete_seleccionado = random.choice(id_cadetes)
    elcadete = db(db.cadete.id == cadete_seleccionado).select().first()
    elprecio = None
    eltotal = 0.0

    # calcular el precio
    lositem = db(db.item.orden == laorden).select()
    for item in lositem:
        elprecio = None
        if item.producto == 'pizza': elprecio = db(db.pizza.id == item.id_producto).select().first().precio
        elif item.producto == 'empanada': elprecio = db(db.empanada.id == item.id_producto).select().first().precio
        elif item.producto == 'bebida': elprecio = db(db.bebida.id == item.id_producto).select().first().precio
        eltotal += item.cantidad * elprecio

    # calcular la hora de entrega
    lahora = laorden.fecha
    td = datetime.timedelta(0,0,0,0,0,1)
    lahoradeentrega = lahora + td    
    
    return dict(orden = laorden.id, cadete = elcadete, total = eltotal, hora_entrega = lahoradeentrega, cliente = elcliente)
    

def pedido():

    if not control_acceso(session):
        raise HTTP(503,"Se alcanzó límite de consultas")


    # usar el usuario por defecto o
    # un error si no hay usuarios (demo)
    elusuario = db(db.auth_user).select().first()
    if not elusuario: raise Exception("No hay usuarios registrados")

    # recuperar datos del cliente
    elcliente = db(db.cliente.usuario == elusuario).select().first()
    if not elcliente: raise Exception("No hay clientes registrados")

    # crear orden
    orden = db.orden.insert(cliente = elcliente)
    laorden = db(db.orden.id == orden).select().first()

    elform = SQLFORM.factory(hidden=dict(orden = orden.id))

    if elform.accepts(request.vars, session):
        return redirect('envio/' + str(elform.request_vars.orden))
    
    # recuperar pizzas / empanadas...
    laspizzas = db(db.pizza).select()
    lasempanadas = db(db.empanada).select()
    lasbebidas = db(db.bebida).select()
    losingredientes = db(db.ingrediente).select()
    lasempanadas_ingredientes = db(db.empanada_ingrediente).select()
    laspizzas_ingredientes = db(db.pizza_ingrediente).select()
    
    # devolver listas de objetos para el view
    return dict(orden = laorden, cliente = elcliente, pizzas_ingredientes = laspizzas_ingredientes, empanadas_ingredientes = lasempanadas_ingredientes, ingredientes = losingredientes, bebidas = lasbebidas, empanadas = lasempanadas, pizzas = laspizzas, form = elform)


@service.json
def pizzas():

    if not control_acceso(session):
        raise HTTP(503,"Se alcanzó límite de consultas")


    lista = []
    undict = None
    respuesta = dict()
    respuesta["page"] = 1
    respuesta["total"] = 1
    respuesta["records"] = 0
    
    for pizza in db(db.pizza).select():
        undict = dict(id = pizza.id, cell = [pizza.id, pizza.nombre, pizza.precio])
        lista.append(undict)
        respuesta["records"] += 1 # cantidad de registros

    respuesta["rows"] = lista
    return respuesta

    
@service.json
def empanadas():

    if not control_acceso(session):
        raise HTTP(503,"Se alcanzó límite de consultas")


    lista = []
    undict = None
    respuesta = dict()
    respuesta["page"] = 1
    respuesta["total"] = 1
    respuesta["records"] = 0
    
    for empanada in db(db.empanada).select():
        undict = dict(id = empanada.id, cell = [empanada.id, empanada.nombre, empanada.precio])
        lista.append(undict)
        respuesta["records"] += 1 # cantidad de registros

    respuesta["rows"] = lista
    return respuesta


@service.json
def bebidas():


    if not control_acceso(session):
        raise HTTP(503,"Se alcanzó límite de consultas")

    lista = []
    undict = None
    respuesta = dict()
    respuesta["page"] = 1
    respuesta["total"] = 1
    respuesta["records"] = 0
    
    for bebida in db(db.bebida).select():
        undict = dict(id = bebida.id, cell = [bebida.id, bebida.nombre, bebida.precio])
        lista.append(undict)
        respuesta["records"] += 1 # cantidad de registros

    respuesta["rows"] = lista
    return respuesta


@service.json
def orden():

    if not control_acceso(session):
        raise HTTP(503,"Se alcanzó límite de consultas")

    la_orden = int(request.vars["orden"])
    lista = []
    undict = None
    respuesta = dict()
    respuesta["page"] = 1
    respuesta["total"] = 1
    respuesta["records"] = 0
    unnombre = None
    unprecio = None
    el_producto = None
    
    for itm in db(db.item.orden == la_orden).select():
        unnombre = None
        if itm.producto == 'pizza':
            el_producto = db(db.pizza.id == itm.id_producto).select().first()
            unnombre = el_producto.nombre
            unprecio = el_producto.precio
            
        elif itm.producto == 'empanada':
            el_producto = db(db.empanada.id == itm.id_producto).select().first()
            unnombre = el_producto.nombre
            unprecio = el_producto.precio
            
        elif itm.producto == 'bebida':
            el_producto = db(db.bebida.id == itm.id_producto).select().first()
            unnombre = el_producto.nombre
            unprecio = el_producto.precio
    
        undict = dict(id = itm.id, cell = [itm.id, itm.producto, itm.orden, unnombre, itm.id_producto, itm.cantidad, unprecio])
        lista.append(undict)
        respuesta["records"] += 1 # cantidad de registros

    respuesta["rows"] = lista
    return respuesta


@service.json
def agregar_item():
    if not control_acceso(session):
        raise HTTP(503,"Se alcanzó límite de consultas")

    la_orden = db(db.orden.id == int(request.vars["orden"])).select().first()
    el_tipo = request.vars.tipo
    el_id = int(request.vars.id)
    db.item.insert(orden = la_orden, producto = el_tipo, id_producto = el_id)
    db.commit()
        
    return str(request.vars)


@service.json
def editar_orden():
    if not control_acceso(session):
        raise HTTP(503,"Se alcanzó límite de consultas")

    mensaje = None

    if request.vars["oper"] == 'edit':
        el_item = db(db.item.id == int(request.vars["id"])).select().first()
        el_item.update_record(cantidad = int(request.vars["cantidad"]))
        db.commit()
        mensaje = "Se modificó el registro nro. " + request.vars["id"]
       
    elif request.vars["oper"] == 'del':
        db(db.item.id == int(request.vars["id"])).delete()
        db.commit()
        mensaje = "Se eliminó el registro nro. " + request.vars["id"]

    return mensaje


@service.json
def calcular_total():
    if not control_acceso(session):
        raise HTTP(503,"Se alcanzó límite de consultas")

    total = None
    total_tmp = 0
    contador = 0
    el_precio = None
    los_item = db(db.item.orden == int(request.vars["orden"])).select()
    for item in los_item:
        el_precio = None
        if item.producto == 'pizza': el_precio = db(db.pizza.id == item.id_producto).select().first().precio
        elif item.producto == 'empanada': el_precio = db(db.empanada.id == item.id_producto).select().first().precio
        elif item.producto == 'bebida': el_precio = db(db.bebida.id == item.id_producto).select().first().precio
        
        total_tmp += el_precio * int(item.cantidad)
        contador += 1
    
    if contador > 0: total = total_tmp
    return total


def ayuda():
    return dict()


def control_acceso(session):
    # recuperar ordenes del día
    hoy = datetime.datetime.now()
    dif = datetime.timedelta(1)
    ayer = hoy - dif
    cant_ordenes = db(db.orden.fecha > ayer).count()
    # si se superó el límite de órdenes devolver false
    if cant_ordenes > 500: return False
    else:
        ordenes = db(db.orden.fecha > ayer).select()

    cant_item = 0
    for orden in ordenes:
        cant_item += db(db.item.orden == orden).count()
        # si hay un exceso salir con estado false
        if cant_item > 2500: return False
    
    return True
