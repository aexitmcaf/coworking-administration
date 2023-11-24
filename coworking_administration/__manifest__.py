{
    "name": "Coworking administration",
    "summary": "Administration system manage booking proces for Coworking",

    "author": "Alex",
    "license": "LGPL-3",
    "website": "https://github.com/aexitmcaf",
    "category": "Customization booking",
    "version": "16.0.1.0.0",
    "depends": ["base"],
    'images': ['static/description/icon.png'],
    "installable": True,

    'data': [
        'security/ir.model.access.csv',
        'security/coworking_groups.xml',
        'security/coworking_security.xml',
        'security/ir_rule.xml',
        'views/coworking_resource_booking_views.xml',
        'views/coworking_resource_booking_tag_views.xml',
        'views/coworking_resource_views.xml',
        'views/coworking_resource_existence_views.xml',
        'views/coworking_menus.xml',
    ],
    'demo': [
        'demo/resource_demo.xml',
    ],
}
