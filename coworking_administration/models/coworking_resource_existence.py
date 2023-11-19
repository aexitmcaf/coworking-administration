from odoo import models, fields, api, exceptions, _


class ResourceExistence(models.Model):
    _name = 'resource.existence'
    _description = 'Resource Existence'

    resource_id = fields.Many2one('resource',
                                  string="Resource Name",
                                  required=True)
    start_datetime = fields.Datetime(string='Start Date & Time', required=True)
    end_datetime = fields.Datetime(string='End Date & Time', required=True)
    existence_status = fields.Selection([
        ('existence', 'Existence'),
        ('booked', 'Not Existence'),
    ], name='Existence Status',
        compute='_compute_existence_status',
        store=True)

    @api.depends('resource_id', 'start_datetime', 'end_datetime')
    def _compute_existence_status(self):
        current_datetime = fields.Datetime.now()
        for existence in self:
            if existence.start_datetime:
                start_datetime = (fields.Datetime.
                                  from_string(existence.
                                              start_datetime))
                if start_datetime < current_datetime:
                    existence.existence_status = 'booked'
                else:
                    booking = self.env['resource.booking'].search([
                        ('name', '=', existence.resource_id.id),
                        ('start_datetime', '<', existence.end_datetime),
                        ('end_datetime', '>', existence.start_datetime),
                    ])
                    if booking:
                        existence.existence_status = 'booked'
                    else:
                        existence.existence_status = 'existence'
            else:
                existence.existence_status = 'booked'

    def create_booking(self):
        existence = self.search([
            ('resource_id', '=', self.resource_id.id),
            ('start_datetime', '=', self.start_datetime),
            ('end_datetime', '=', self.end_datetime),
        ])
        if existence.existence_status == 'existence':
            return {
                'name': 'Show booking',
                'type': 'ir.actions.act_window',
                'res_model': 'resource.booking',
                'view_mode': 'form',
                'view_id': False,
                'target': 'new',
            }
        raise exceptions.UserError(_("Resource is not existence for"
                                     " the selected time period."))

    @api.constrains('start_datetime', 'end_datetime')
    def check_start_end_dates(self):
        for booking in self:
            if booking.start_datetime and booking.end_datetime:
                if booking.end_datetime < booking.start_datetime:
                    raise exceptions.ValidationError(_("End date cannot"
                                                       " be before the"
                                                       " start date."))


class ResourceExistenceByResource(models.Model):
    _name = 'resource.existence.by.resource'
    _description = 'Resource Existence By Resource'

    resource_id = fields.Many2one('resource',
                                  string="Resource Name",
                                  required=True)
    related_bookings = fields.Many2many('resource.booking',
                                        compute='_compute_related_bookings')

    @api.depends('resource_id')
    def _compute_related_bookings(self):
        for i in self:
            i.related_bookings = self.env['resource.booking'].search([
                ('name', '=', i.resource_id.id),
            ])

    def show_related_bookings(self):
        self.ensure_one()
        return {
            'name': 'Related Bookings',
            'type': 'ir.actions.act_window',
            'res_model': 'resource.booking',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.related_bookings.ids)],
            'target': 'current',
        }


class ResourceExistenceByDate(models.Model):
    _name = 'resource.existence.by.dates'
    _description = 'Resource Existence By Date'

    start_date = fields.Datetime(string='Start Date & Time', required=True)
    end_date = fields.Datetime(string='End Date & Time', required=True)
    related_bookings = fields.Many2many('resource.booking',
                                        compute='_compute_related_bookings')

    @api.depends('start_date', 'end_date')
    def _compute_related_bookings(self):
        for i in self:
            i.related_bookings = self.env['resource.booking'].search([
                ('start_datetime', '<', i.end_date),
                ('end_datetime', '>', i.start_date),
            ])

    def show_related_bookings(self):
        self.ensure_one()
        return {
            'name': 'Related Bookings',
            'type': 'ir.actions.act_window',
            'res_model': 'resource.booking',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.related_bookings.ids)],
            'target': 'current',
        }

    @api.constrains('start_date', 'end_date')
    def check_start_end_dates(self):
        for booking in self:
            if booking.start_date and booking.end_date:
                if booking.end_date < booking.start_date:
                    raise exceptions.ValidationError(_("End date cannot"
                                                       " be before the"
                                                       " start date."))
