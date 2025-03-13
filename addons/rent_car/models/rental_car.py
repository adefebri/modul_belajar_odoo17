from odoo import fields, models

class RentalCar(models.Model):
    _name = 'rental.car'
    _description = 'Mobil rental'


    name = fields.Char(string= 'Mobil' ,required=True)
    brand = fields.Char(string='Brand',required=True)
    tahun = fields.Char(string='Year')
    harga_sewa = fields.Float(string='Harga' ,required=True)
    status = fields.Selection([('available','Available'), ('booked','Booked')],
                               string='Status',
                               default='available' )
    image_128 = fields.Binary(string="Image", attachment=True)  