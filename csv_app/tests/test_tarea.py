import unittest
from odoo.tests import TransactionCase, tagged, common
from odoo.exceptions import UserError, AccessError, AccessDenied, Warning, ValidationError

class TestModuloSaldo(common.TransactionCase):
    def setUp(self):
        super(TestModuloSaldo, self).setUp()
        self.Users = self.env['res.users'].with_context({'no_reset_password': True})
        self.tarea_obj =  self.env['cv.tarea']

        self.user_public = self.Users.create({
            'name': 'Bert Tartignole',
            'login': 'bert',
            'email': 'b.t@example.com',
            'signature': 'SignBert',
            'notification_type': 'email',
            'pm_pedagogia':10,
            'pm_etico':50,
            'pm_academico':40,
            'groups_id': [(6, 0, [self.env.ref('csv_app.res_groups_docente').id])]})

        self.task_1 = self.env['cv.tarea'].create({
            'name': 'barrer',
            'date_init': '2020-10-01 16:00:00',
            'date_fin': '2020-10-14 16:00:00',
            'state': 'pendiente',
            'rating': 'bajo',
            'user_id': self.user_public.id})

    def test_task_model_exists(self):
        self.assertTrue(self.tarea_obj._name in self.env)

    def test_task_creates_with_valid_data(self):
        task = self.tarea_obj.create({'name': 'barrer',
            'date_init': '2020-10-01 16:00:00',
            'date_fin': '2020-10-14 16:00:00',
            'state': 'pendiente',
            'rating': 'bajo',
            'user_id': self.user_public.id})
        self.assertTrue(bool(self.tarea_obj.search([('id', '=', task.id)], limit=1)))

    #def test_task_creation_throws_exception_with_invalid_data(self):
        #with self.assertRaises(ValidationError):
            #self.tarea_obj.create({'name':500,
                #'date_init': '2020-10-01 16:00:00',
                #'date_fin': '2020-10-14 16:00:00',
                #'state': 'pendiente',
                #'rating': 'bajo',})


    def test_task_unlink_groups(self):
        test_tarea = self.env['cv.tarea'].create({
            'name': 'barrer',
            'date_init': '2020-10-01 16:00:00',
            'date_fin': '2020-10-14 16:00:00',
            'state': 'pendiente',
            'rating': 'bajo',
        })
        self.assertTrue(test_tarea, msg=None)
        self.assertTrue(test_tarea.unlink(), msg=None)

    def test_task_method_compute_valoracion_docente(self):
        self.user_public._compute_valoracion_docente()
        self.assertEqual(self.user_public.total_val, 100)

    def test_user_method_check_pm_etico(self):
        user_public = self.Users.create({
            'name': 'Bert Tartignole',
            'login': 'barce',
            'email': 'b.t@example.com',
            'signature': 'SignBert',
            'pm_etico': 50,
            'notification_type': 'email',
            'groups_id': [
                (6, 0, [self.env.ref('csv_app.res_groups_docente').id])]})
        self.assertRaises(ValidationError, user_public._check_pm_etico(), -3)

    def test_user_method_check_pm_pedagogia(self):
        user_public = self.Users.create({
            'name': 'Bert Tartignole',
            'login': 'barce2',
            'email': 'b.t@example.com',
            'signature': 'SignBert',
            'pm_pedagogia': 50,
            'notification_type': 'email',
            'groups_id': [
                (6, 0, [self.env.ref('csv_app.res_groups_docente').id])]})
        self.assertRaises(ValidationError, user_public._check_pm_pedagogia(), -3)

    def test_user_method_check_pm_academico(self):
        user_public = self.Users.create({
            'name': 'Bert Tartignole',
            'login': 'barce1',
            'email': 'b.t@example.com',
            'signature': 'SignBert',
            'pm_academico': 50,
            'notification_type': 'email',
            'groups_id': [
                (6, 0, [self.env.ref('csv_app.res_groups_docente').id])]})
        self.assertRaises(ValidationError, user_public._check_pm_academico(), -3)