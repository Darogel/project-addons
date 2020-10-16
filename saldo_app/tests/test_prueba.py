import unittest
from odoo.tests import TransactionCase, tagged, common
from odoo.exceptions import Warning

class TestModuloSaldo(common.TransactionCase):
    def setUp(self):
        super(TestModuloSaldo, self).setUp()

    def test_data(self):
        test_movimiento_1 = self.env['sa.movimiento'].create({
            'name':'barrer',
            'type_mov':'ingreso',
            'amount':500,
        })

        self.assertEqual(test_movimiento_1.amount, 500)
        print("Test Passed")

