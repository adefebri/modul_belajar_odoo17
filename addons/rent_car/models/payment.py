from odoo import api, fields, models
import datetime

class Pembayaran(models.Model):
    _name = 'pembayaran.mobil'
    _description = 'Pembayaran mobil'


    pembayaran_id = fields.Many2one('pemesanan.mobil',string= 'Pemesanan' ,required=True)
    harga = fields.Float(string = 'Harga', related='pembayaran_id.total_harga_sewa')
    metode_pembayaran = fields.Selection([('cash', 'Cash'),
                                           ('bank','Bank Transfer'),
                                           ('card', 'Credit Card')],
                                           string='Metode Pembayaran',
                                           required = True
                                           )
    status = fields.Selection([('pending','Pending'),
                               ('success','Success')],
                               string='Status Pembayaran',
                               default='pending')   
    default=lambda self: self._default_name()



    @api.model

    def create(self, vals):
        # Panggil method create dari superclass
        payment = super(Pembayaran, self).create(vals)

        # Ubah status mobil menjadi 'booked'
        if payment.status == 'success':
            payment.pembayaran_id.write({'status_book': 'confirmed'})

        return payment

    def write(self, vals):
        # Panggil method write dari superclass

        result = super(Pembayaran, self).write(vals)
    
        # Jika status diubah menjadi 'completed'

        if 'status' in vals and vals['status'] == 'success':
            # Ubah status mobil menjadi 'confirmed'
            self.pembayaran_id.write({'status_book': 'confirmed'})

        return result
    
    def unlink(self):
        # Kembalikan status mobil ke 'available' ketika pemesanan dihapus
        for record in self:
            record.pembayaran_id.write({'status_book': 'cancelled'})
        return super(Pembayaran, self).unlink()