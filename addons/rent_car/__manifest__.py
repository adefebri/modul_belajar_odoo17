{
    'name': 'Rental Car Management',
    'version': '1.0',
    'summary': 'Manage car rentals, customers, bookings, and payments',
    'description': 'A module to manage car rental operations in Odoo 17',
    'author': 'Littlemust',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/rental_car_views.xml',
        'views/customer_views.xml',
        'views/booking_views.xml',
        'views/payment_views.xml',
    ],
    'installable': True,
    'application': True,
}