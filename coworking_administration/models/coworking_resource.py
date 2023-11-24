from odoo import models, fields, api


class CoworkingResource(models.Model):
    _name = 'resource'
    _description = 'Coworking Resource'

    name = fields.Char(string='Resource name', required=True)
    resource_type = fields.Many2one(
        'resource.type',
        string="Resource Type ", required=True)

    resource_owner = fields.Char(string='Resource owner', required=True)
    image = fields.Binary(string='')
    booking_ids = fields.One2many('resource.booking',
                                  'name',
                                  string='Booking')
    confirmed_bookings = fields.One2many('resource.booking',
                                         'name',
                                         compute='_compute_confirmed')
    cancelled_bookings = fields.One2many('resource.booking',
                                         'name',
                                         compute='_compute_cancelled')
    resource_tags = fields.Many2many('resource.tag',
                                     string='Resource Tags ',
                                     help="Select one or more resource tags",
                                     widget='many2many_tags')

    @api.depends('booking_ids')
    def _compute_confirmed(self):
        for record in self:
            record.confirmed_bookings = record.booking_ids.filtered(
                lambda r: r.booking_status == 'confirmed')

    @api.depends('booking_ids')
    def _compute_cancelled(self):
        for record in self:
            record.cancelled_bookings = record.booking_ids.filtered(
                lambda r: r.booking_status == 'cancelled')


class ResourceType(models.Model):
    _name = 'resource.type'
    _description = 'Resource Type'

    name = fields.Char(string='Resource Type', required=True)

    _sql_constraints = [
        ('unique_resource_type', 'UNIQUE (name)',
         'A resource type with the same name already exists.'),
    ]


class ResourceTag(models.Model):
    _name = 'resource.tag'
    _description = 'Resource Tag'

    name = fields.Char(string='Resource Tag', required=True)
    color = fields.Integer(string="Color ")

    _sql_constraints = [
        ('unique_resource_tag', 'UNIQUE (name)',
         'A resource type with the same name already exists.'),
    ]
