# -*- coding: utf-8 -*
{
    'name': 'Cafeina',
    'version': '1.0',
    'author': 'José M Martinez',
    'description': "",
    'summary': 'Adatación para la empresa Cafeina',
    'category': '',
    'website': 'http://hackeando.net',
    'depends': [
        'base',
        'sale', 
        'project', 
        'project_timesheet', 
        'auditoria'
    ],
    'data': [
        'sequence/minuta_sequence.xml', 
        'view/calculator_view.xml',
        'view/project_view.xml', 
        'view/minuta_view.xml', 
        'view/planeacion_view.xml', 
        'view/obra_view.xml', 
        'view/financiera_view.xml', 
        'view/saleorder_view.xml', 
        'view/financiera2_view.xml'
    ],
    'js': [
    ],
    'css': [
    ],
    'qweb': [
    ],
    'init_xml': [

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
