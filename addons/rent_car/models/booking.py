from odoo import fields, api, models, _
from odoo.exceptions import ValidationError
import datetime

class Pemesanan(models.Model):
    _name = 'pemesanan.mobil'
    _description = 'Booking'


    mobil_id = fields.Many2one('rental.car',string= 'Mobil Rental' ,required=True)
    customer_id = fields.Many2one('rent.customer',string='Customer',required=True)
    name = fields.Char(string='Booking Reference', required=True, copy=False,default=lambda self: self._default_name(), readonly=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    status_book = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')    
    total_harga_sewa = fields.Float(string = 'Total Harga', compute = '_compute_total_price', store = True)

    def _default_name(self):
        return f"Book_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    @api.depends('start_date', 'end_date','mobil_id.harga_sewa')
    def _compute_total_price(self):
        for record in self:
           if record.start_date and record.end_date and record.mobil_id:
               durasi = (record.end_date - record.start_date).days
               record.total_harga_sewa = durasi * record.mobil_id.harga_sewa


    @api.model
    def create(self, vals):
        car = self.env['rental.car'].browse(vals.get('mobil_id'))
        customer = self.env['rent.customer'].browse(vals.get('customer_id'))
        print('================================================')
        print(car.name)
        print(customer.name)
        if car.status != 'available':
            raise ValidationError("Mobil ini sudah dipesan. Silakan pilih mobil lain.")
        booking_ref = f"CAR-{car.name}-{customer.name}-{datetime.datetime.now().strftime('%Y%m%d')}"
        vals['name'] = booking_ref
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
    
    def unlink(self):
        # Kembalikan status mobil ke 'available' ketika pemesanan dihapus
        for record in self:
            record.mobil_id.write({'status': 'available'})
        return super(Pemesanan, self).unlink()
    


    def action_complete(self):
        # Ubah status pemesanan menjadi 'completed'
        self.write({'status': 'completed'})
        # Ubah status mobil menjadi 'available'
        self.car_id.write({'status': 'available'})


    def action_status_book_completed(self):
        for task in self:
            if task.status_book == "confirmed":
                task.write({
                    "status_book": "completed",
                })

    def action_status_book_cancelled(self):
        for task in self:
            task.write({
                    "status_book": "cancelled",
                })
            
    def action_status_book_confirmed(self):
        for task in self:
            task.write({
                    "status_book": "confirmed",
                })