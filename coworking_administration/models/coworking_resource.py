from odoo import models, fields, api, exceptions, _


class CoworkingResource(models.Model):

    _name = 'coworking.administration.resource'
    _description = 'Coworking Resource'

    name = fields.Char(string='Resource', )
    title = fields.Char(string='Title ', required=True)

