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

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae://mynamespace')             # connect to Google BigTable
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import *

import datetime

mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:096c0573-5102-4be2-a6e4-93afbd8878d8'   # before define_tables()
auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

#########################################################################
## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
# from gluon.contrib.login_methods.rpx_account import RPXAccount
# auth.settings.actions_disabled=['register','change_password','request_reset_password']
# auth.settings.login_form = RPXAccount(request, api_key='...',domain='...',
#    url = "http://localhost:8000/%s/default/user/login" % request.application)
## other login methods are in gluon/contrib/login_methods
#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('ingrediente', Field('tipo', requires = IS_IN_SET(
['salsa', 'queso', 'condimento', 'otro']
)), Field('nombre')
)

db.define_table('bebida' , Field('tipo', requires = IS_IN_SET(
['jugo', 'alcohólica', 'gaseosa']
)), Field('nombre'), Field('medida'), Field('precio', 'double'))

db.define_table('empanada', Field('nombre'), Field('medida'), Field('precio', 'double'))

db.define_table('pizza', Field('nombre'), Field('medida'), Field('precio', 'double'))

db.define_table('cadete', Field('nombre'), Field('documento'), Field('foto', 'upload'))

db.define_table('cliente', Field('nombre'), Field('direccion'), Field('telefono'), Field('usuario', 'reference auth_user', unique = True))

db.define_table('orden', Field('ticket'), Field('cadete', 'reference cadete'), Field('entregada', 'boolean', default = False), Field('cliente', 'reference cliente'), Field('fecha', 'datetime', default = request.now))

db.define_table('item', Field('producto', requires = IS_IN_SET(['pizza', 'empanada', 'bebida'])), Field('orden', 'reference orden'), Field('id_producto', 'integer'), Field('cantidad', 'integer', default=1))

db.define_table('cajero', Field('usuario', 'reference auth_user', unique = True))

db.define_table('pizza_ingrediente', Field('ingrediente', 'reference ingrediente'), Field('pizza', 'reference pizza'))

db.define_table('empanada_ingrediente', Field('ingrediente', 'reference ingrediente'), Field('empanada', 'reference empanada'))
