from odoo import models, fields, api, exceptions, _


class BookingTag(models.Model):
    _name = 'resource.booking.tag'
    _description = 'Booking Tag'

    name = fields.Char(string='Booking Tag', required=True)
    description = fields.Text(string='Description ')
    color = fields.Integer(string='Color ')

    _sql_constraints = [
        ('unique_booking_tag', 'UNIQUE (name)',
         'A booking tag with the same type already exists.'),
    ]


class ResourceBooking(models.Model):
    _name = 'resource.booking'
    _description = 'Resource Booking'

    title = fields.Char(string='Title ', required=True)
    name = fields.Many2one('resource',
                           string='Resource Name', options={'no_create': True})
    resource_type = fields.Many2one('resource.type',
                                    string='Resource Type', options={'no_create': True})
    start_datetime = fields.Datetime(string='Start Date & Time',
                                     default=lambda self:
                                     fields.Datetime.now(),
                                     help="Store the "
                                          "current date and time",
                                     required=True)
    end_datetime = fields.Datetime(string='End Date & Time',
                                   help="This field will store "
                                        "the end date and time "
                                        "of the event or task.",
                                   required=True)
    creator = fields.Char(string='Created By',
                          default=lambda self: self.env.user.name,
                          required=True)
    user_id = fields.Integer(string='User ID',
                             default=lambda self: self.env.user.id,
                             required=True)
    booking_status = fields.Selection([
        ('pending', 'Pending '),
        ('confirmed', 'Confirmed '),
        ('cancelled', 'Cancelled '),
    ],
        string='Booking Status ',
        default='pending',
        help="This field represents the status of the booking.")
    resource_description = fields.Text(string="booking Description",
                                       required=True)

    booking_tag_id = fields.Many2many(
        'resource.booking.tag',
        string="Booking Tag",
        required=True,
        widget='many2many_tags')

    def update_booking_status_cancel(self):
        self.write({'booking_status': 'cancelled'})

    def update_booking_status_confirm(self):
        self.write({'booking_status': 'confirmed'})

    @api.model
    def create(self, vals_list):
        vals_list['creator'] = self.env.user.name
        return super().create(vals_list)

    @api.constrains('name', 'start_datetime', 'end_datetime')
    def check_overlapping_bookings(self):
        for booking in self:
            overlapping = (self.env['resource.booking'].search([
                ('id', '!=', booking.id),
                ('name', '=', booking.name.id),
                ('start_datetime', '<', booking.end_datetime),
                ('end_datetime', '>', booking.start_datetime),
            ]))
            if overlapping:
                raise exceptions.ValidationError(_("Overlapping bookings"
                                                   " are not allowed."))

    @api.constrains('start_datetime', 'end_datetime')
    def check_start_end_dates(self):
        for booking in self:
            if booking.start_datetime and booking.end_datetime:
                if booking.end_datetime < booking.start_datetime:
                    raise exceptions.ValidationError(_("End date cannot"
                                                       " be before the"
                                                       " start date."))

    @api.constrains('start_datetime')
    def check_future_start_date(self):
        for i in self:
            if i.start_datetime and i.start_datetime < fields.Datetime.now():
                raise exceptions.ValidationError(_("Bookings for "
                                                   "past dates are "
                                                   "not allowed."))

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            return {'domain': {'name': [('resource_type', '=', self.name.resource_type.id), ('id', '!=', False)]}}

    @api.onchange('resource_type')
    def _onchange_resource_type(self):
        if self.name:
            return {'domain': {'name': [('resource_type', '=', self.resource_type.id), ('id', '!=', False)]}}