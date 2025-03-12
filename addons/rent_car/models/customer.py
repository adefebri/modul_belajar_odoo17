from odoo import fields, models

class Customer(models.Model):
    _name = 'rent.customer'
    _description = 'Penyewa mobil'


    name = fields.Char(string= 'Customer' ,required=True)
    alamat = fields.Text(string='Alamat',required=True)
    no_telp = fields.Char(string='Telp',required=True)
    email = fields.Char(string='Email')
