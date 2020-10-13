from odoo import models
import logging
import base64
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz
import tempfile
import csv
_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    def remove_finish_import_crons(self):
        master_partners = self.env['import.part.master'].search(
            ['|', ('status', '=', 'imported'), ('status', '=', 'failed')])
        # Remove completed crons
        for master_part in master_partners:
            if master_part.cron_id:
                master_part.cron_id.unlink()
        # Remove the Import status lines
        imported_master_part = self.env['import.part.master'].search(
            [('status', '=', 'imported')])
        imported_master_part.unlink()

    def import_data(self, part_master_id=False):
        if part_master_id:
            part_master = self.env[
                'import.part.master'].browse(part_master_id)
            total_success_import_record = 0
            total_failed_record = 0
            list_of_failed_record = ''
            datafile = part_master.file
            file_name = str(part_master.filename)
            user_obj = self.env['res.users']
            state_obj = self.env['res.country.state']
            country_obj = self.env['res.country']
            try:
                if not datafile or not \
                        file_name.lower().endswith(('.csv')):
                    list_of_failed_record += "Please Select a.csv or its compatible file to Import."
                    _logger.error(
                        "Please Select a .csv or its compatible file to Import.")
                if part_master.type == 'csv':
                    if not datafile or not file_name.lower().endswith(('.csv')):
                        list_of_failed_record += "Please Select an .csv or its compatible file to Import."
                        _logger.error(
                            "Please Select an .csv or its compatible file to Import.")
                    file_path = tempfile.gettempdir() + '/import.csv'
                    f = open(file_path, 'wb+')
                    f.write(base64.decodestring(part_master.file))
                    f.close()

                    archive = csv.DictReader(open(file_path))
                    archive_lines = [line for line in archive]
                    count = 1
                    for line in archive_lines:
                        try:
                            count += 1
                            user_vals = {
                                'name': line.get('name'),
                                'phone': line.get('phone') or '',
                                'password': line.get('password') or '',
                                'login': line.get('login') or '',
                                'email': line.get('email'),
                                'pm_pedagogia': line.get('pm_pedagogia'),
                                'pm_etico': line.get('pm_etico'),
                                'pm_academico': line.get('pm_academico')
                            }
                            state = state_obj.search(
                                [('name', '=', line.get('state'))])
                            country = country_obj.search(
                                [('name', '=', line.get('country'))])
                            user_vals['state_id'] = state.id or ''
                            user_vals[
                                'country_id'] = country.id or ''

                            if part_master.operation == 'create':
                                user_obj.create(user_vals)
                            else:
                                part_id = self.env['res.users'].search(
                                    [('name', '=', line.get('name', ''))], limit=1)
                                if not part_id:
                                    part_id = user_obj.create(
                                        user_vals)
                                else:
                                    part_id.write(user_vals)
                            total_success_import_record += 1
                        except Exception as e:
                            total_failed_record += 1
                            list_of_failed_record += line
                            _logger.error("Error at %s" % str(line))
            except Exception as e:
                list_of_failed_record += str(e)
            try:
                file_data = base64.b64encode(
                    list_of_failed_record.encode('utf-8'))
                part_master.status = 'imported'

                datetime_object = datetime.strptime(
                    str(part_master.create_date), '%Y-%m-%d %H:%M:%S.%f')

                start_date = datetime.strftime(
                    datetime_object, DEFAULT_SERVER_DATETIME_FORMAT)
                self._cr.commit()
                now_time = datetime.now()
                user_tz = self.env.user.tz or str(pytz.utc)
                local = pytz.timezone(user_tz)
                start_date_in_user_tz = datetime.strftime(pytz.utc.localize(
                    datetime.strptime(str(start_date), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(
                    local), DEFAULT_SERVER_DATETIME_FORMAT)
                end_date_in_user_tz = datetime.strftime(pytz.utc.localize(
                    now_time).astimezone(local),
                    DEFAULT_SERVER_DATETIME_FORMAT)
                self.env['import.part.history'].create({
                    'total_success_count': total_success_import_record,
                    'total_failed_count': total_failed_record,
                    'file': file_data,
                    'file_name': 'report_importazione.txt',
                    'type': part_master.type,
                    'import_file_name': part_master.filename,
                    'start_date': start_date_in_user_tz,
                    'end_date': end_date_in_user_tz,
                    'operation': part_master.operation,
                })
                if part_master.user_id:
                    message = "Import process is completed. Check in Imported Partner History if all the partners have" \
                              " been imported correctly. </br></br> Imported File: %s </br>" \
                              "Imported by: %s" % (
                                  part_master.filename, part_master.user_id.name)
                    part_master.user_id.notify_partner_info(
                        message, part_master.user_id, sticky=True)
                self._cr.commit()
            except Exception as e:
                part_master.status = 'failed'
                _logger.error(e)
                self._cr.commit()

    def notify_partner_info(self, message, user, sticky=False):
        self._notify_partner_channel(message, user, sticky)

    def _notify_partner_channel(self, message, user, sticky):
        user.notify_info(
            message=message, title="Notification for Import Partner",
            sticky=True)