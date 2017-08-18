# -*- coding: utf-8 -*-
{
    "name": "Auditoria de Seguridad",
    "version": "1.0",
    "author": "Jose M Martz",
    "category": "",
    "description": """
    Modulo de Auditoria
    """,
    "website": "",
    "license": "AGPL-3",
    "depends": [
         'base',
         'hr',
    ],
    "demo": [
    ],
    "data": [
        'sequence/auditoria_sequence.xml',
        'sequence/noconformidad_sequence.xml',
        'sequence/rac_sequence.xml',
        'security/groups.xml',
        'view/auditoria.xml',
        'view/auditoria_resultado_view.xml',
        'view/no_conformidad.xml',
        'view/rac_view.xml',
        'workflow/auditoria_workflow.xml',
        'workflow/checklist_workflow.xml',
        'workflow/no_conformidad.xml',
        'workflow/resultado_workflow.xml',
    ],
    'css': [],
    'test': [],
    "installable": True,
    "active": False,
}