{
    "name": "Coworking administration",
    "summary": "Administration system will help to manage booking proces for Coworking places",

    "author": "Alex",
    "license": "LGPL-3",
    "website": "https://github.com/",
    "category": "Customization booking",
    "version": "16.0.1.0.0",
    "depends": ["base"],
    'images': ['static/description/icon.png'],
    "installable": True,

    'data': [
        'security/ir.model.access.csv',
        'views/coworking_administration_menus.xml',
        'views/coworking_administration_resource_views.xml',

    ],
    'demo': [
        'demo/resource_demo.xml',
    ],
}
