from odoo import models, api
from datetime import datetime

class ReporteTareas(models.AbstractModel):
    _name = "report.pm1_app.report_plan_mejoras"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["cv.informe"].browse(docids)
        docargs = {
            "docs":docs,
            "fecha":datetime.now().strftime("%m-%d-%Y"),
        }
        return docargs

