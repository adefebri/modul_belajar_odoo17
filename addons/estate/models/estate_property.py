from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name= 'estate.property'
    _description= 'Estate Property'

    name = fields.Char(string='Title',required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(sting='Available From',copy=False,default=lambda self: fields.Date.today() + relativedelta(months=+3))
    expected_price = fields.Float(required=True)
    selling_price  = fields.Float(readonly=True,copy=False)
    bedrooms  = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (m²)')
    facades = fields.Integer()
    garage = fields.Boolean()  
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
     [('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')]
    )
    #reserve fields
    active = fields.Boolean(string='active',default=False)
    state  =fields.Selection([
        ('new','New'),
        ('offer_received','Offer Received'),
        ('offer_accepted','Offer Accepted'),
        ('sold','Sold'),
        ('canceled','Canceled')
    ],default='new', copy=False)         