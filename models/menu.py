# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('customize me!')

#http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'hexa662@gmail.com'
response.meta.description = 'The pythonic pizza point of sale for web2py'
response.meta.keywords = 'web2py, python, pizza shop'
response.meta.generator = 'Web2py Enterprise Framework'
response.meta.copyright = 'Copyright 2007-2011'

##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
    (T('Inicio'), False, URL(request.application,'default','index'), []),
    (T('Nuevo pedido'), False, URL(request.application,'default','pedido'), []),
    (T('Ayuda'), False, URL(request.application,'default','ayuda'), []),
    (T('hexa662'), False, 'http://sites.google.com/site/hexa662', []),
    (T('Interfaces Web'), False, 'http://sites.google.com/site/hexa662/productos-web', []),
    (T('Más apicaciones'), False, 'http://sites.google.com/site/hexa662/productos-web#ejemplos', [])    
    ]

##########################################
## this is here to provide shortcuts
## during development. remove in production
##
## mind that plugins may also affect menu
##########################################

#########################################
## Make your own menus
##########################################

##########################################
## this is here to provide shortcuts to some resources
## during development. remove in production
##
## mind that plugins may also affect menu
##########################################
