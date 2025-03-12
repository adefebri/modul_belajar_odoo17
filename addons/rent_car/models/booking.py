from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Pemesanan(models.Model):
    _name = 'pemesanan.mobil'
    _description = 'Booking'


    mobil_id = fields.Many2one('rental.car',string= 'Mobil Rental' ,required=True)
    customer_id = fields.Many2one('rent.customer',string='Customer',required=True)
    name = fields.Char(string='Booking Reference', required=True, copy=False)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    status_book = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')    
    total_harga_sewa = fields.Float(string = 'Total Harga', compute = '_compute_total_price', store = True)

    @api.depends('start_date', 'end_date','mobil_id.harga_sewa')
    def _compute_total_price(self):
        for record in self:
           if record.start_date and record.end_date and record.mobil_id:
               durasi = (record.end_date - record.start_date).days
               record.total_harga_sewa = durasi * record.mobil_id.harga_sewa


    @api.model
    def create(self, vals):
        car = self.env['rental.car'].browse(vals.get('mobil_id'))
        if car.status != 'available':
            raise ValidationError("Mobil ini sudah dipesan. Silakan pilih mobil lain.")
        booking = super(Pemesanan, self).create(vals)
        booking.mobil_id.write({'status': 'booked'})
        return booking
    
    def write(self, vals):
        # Panggil method write dari superclass
        old_car = self.mobil_id
        result = super(Pemesanan, self).write(vals)
    
        # Jika status diubah menjadi 'completed'

        if 'status_book' in vals and vals['status_book'] == 'completed':
            # Ubah status mobil menjadi 'available'
            self.mobil_id.write({'status': 'available'})
        elif 'status_book' in vals and vals['status_book'] == 'cancelled':
            # Ubah status mobil menjadi 'available'
            self.mobil_id.write({'status': 'available'})
        elif 'status_book' in vals and vals['status_book'] == 'confirmed':
            # Ubah status mobil menjadi 'booked'
            print(old_car.status)
            self.mobil_id.write({'status': 'booked'})


        # Jika mobil diubah, pastikan status mobil diperbarui
        if 'mobil_id' in vals:              
                new_car = self.env['rental.car'].browse(vals['mobil_id'])
                # Validasi: Pastikan mobil baru tersedia
                if new_car.status != 'available':
                    raise ValidationError("Mobil ini sudah dipesan. Silakan pilih mobil lain.")

                if old_car and old_car != new_car:
                    old_car.write({'status': 'available'})

                new_car.write({'status': 'booked'})
        return result