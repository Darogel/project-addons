self.assertTrue(auditlog_log.search([
            ('model_id', '=', methoo),
            ('method', '=', 'create'),
            ('user_id', '=', self.user_public.id)
        ]).ensure_one())
        test_tarea.unlink()
        self.assertTrue(auditlog_log.search([
             ('model_id', '=', methoo),
             ('method', '=', 'unlink'),
             ('res_id', '=', test_tarea.id),
             ('user_id', '=', self.user_public.id)
             ]).ensure_one())

    def test_delete_project_with_tasks(self):
        #self.assertRaises(AccessError, self.env['cv.tarea'].with_user(self.user_public).read)
        #with self.assertRaises(AccessError, self.env['cv.tarea'].with_user(self.user_public).read):
        self.groups_model_id = self.env.ref('csv_app.model_cv_tarea').id
        self.groups_rule = self.env['auditlog.rule'].create({
            'name': 'testrule for groups',
            'model_id': self.groups_model_id,
            'log_read': True,
            'log_create': False,
            'log_write': False,
            'log_unlink': False,
            'log_type': 'full',
        })

        test_tarea = self.env['cv.tarea'].create({
            'name': 'barrer',
            'date_init': '2020-10-01 16:00:00',
            'date_fin': '2020-10-14 16:00:00',
            'state': 'pendiente',
            'rating': 'bajo',
        })
        self.assertTrue(test_tarea,msg=None)
        self.assertTrue(test_tarea.unlink(), msg=None)
        # click on the archive button
        #self.project_pigs.write({'active': False})

        #with self.assertRaises(UserError):
            #self.project_pigs.unlink()

