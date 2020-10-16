import unittest
from odoo.tests import TransactionCase, tagged, common
from odoo.exceptions import UserError, AccessError, AccessDenied, Warning

class TestModuloSaldo(common.TransactionCase):
    def setUpC(self):
        super(TestModuloSaldo, self).setUp()

        user_group_project_user_docente = self.env.ref(
            'csv_app.res_groups_docente')
        user_group_project_user_admin = self.env.ref(
            'csv_app.res_groups_administrador')

        Users = self.env['res.users'].with_context({'no_reset_password': True})
        self.user_public = Users.create({
            'name': 'Bert Tartignole',
            'login': 'bert',
            'email': 'b.t@example.com',
            'signature': 'SignBert',
            'notification_type': 'email',
            'groups_id': [(6, 0, [self.env.ref('csv_app.res_groups_docente').id])]})

        self.task_1 = self.env['cv.tarea'].create({
            'name': 'barrer',
            'date_init': '2020-10-01 16:00:00',
            'date_fin': '2020-10-14 16:00:00',
            'state': 'pendiente',
            'rating': 'bajo',
            'user_id': self.user_public.id})

    def test_data(self):
        test_tarea = self.env['cv.tarea'].create({
            'name': 'barrer',
            'date_init': '2020-10-01 16:00:00',
            'date_fin': '2020-10-14 16:00:00',
            'state': 'pendiente',
            'rating': 'bajo',
        })
        self.assertEqual(test_tarea.rating, 'bajo')
        print("Test Passed")

    def test_delete_project_with_tasks(self):
        #self.assertRaises(AccessError, self.env['cv.tarea'].with_user(self.user_public).read)
        #with self.assertRaises(AccessError, self.env['cv.tarea'].with_user(self.user_public).read):
        self.task_1.unlink()

        # click on the archive button
        #self.project_pigs.write({'active': False})

        #with self.assertRaises(UserError):
            #self.project_pigs.unlink()

