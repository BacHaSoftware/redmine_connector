import odoo
from odoo import _
import logging
from odoo import models, fields, api
from datetime import date, datetime, timedelta
from redminelib import Redmine

import slack, html
from htmlslacker import HTMLSlacker

_logger = logging.getLogger(__name__)

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    redmine_activity = fields.Char('Redmine activity')

class BHAPILogs(models.Model):
    _name = 'bh.api.logs'
    _description = 'BHS API Logs'

    log_date = fields.Datetime(string='Log date')
    type = fields.Selection([('redmine','Redmine')], string='Type')
    logs = fields.Text(string='Logs')

    # Redmine: Syn spent time data
    @api.model
    def syn_timesheet_redmine(self, days=0, from_date=False, to_date=False):
        redmine_page = self.env['ir.config_parameter'].sudo().get_param('redmine_page')
        redmine_api_key = self.env['ir.config_parameter'].sudo().get_param('redmine_api_key')
        if redmine_page and redmine_api_key:
            redmine = Redmine(redmine_page, key=redmine_api_key)

            # lấy tất cả người dùng trên redmine
            users = redmine.user.all()
            users_not_in_odoo = []
            users_not_in_odoo_not_log_time = []

            #lấy khoảng thời gian lọc dữ liệu redmine
            if from_date and to_date:
                to_date_filter = to_date
                from_date_filter = from_date
            else:
                to_date_filter = date.today().isoformat()
                from_date_filter = (date.today() - timedelta(days=days)).isoformat()

            for user in users:
                odoo_user = self.env['res.users'].sudo().search([('login', '=', user.mail)])
                odoo_emp = self.env['hr.employee'].sudo().search([('work_email', '=', user.mail)])
                # neu nguoi dung nay co tren odoo
                if odoo_user or odoo_emp:
                    time_entries = redmine.time_entry.filter(user_id=user.id, from_date=from_date_filter, to_date=to_date_filter)
                    for st in time_entries:
                        issue_detail = redmine.issue.get(st.issue)
                        # tao task odoo
                        check_task = self.env['project.task'].sudo().search([('name', '=', '#%d' % st.issue)], limit=1)
                        task_data = {
                            'project_id': self.env.ref('bhs_connector_redmine.bh_project_redmine').id,
                            'stage_id': self.env.ref('bhs_connector_redmine.bh_project_task_type_redmine').id,
                            'description': issue_detail.subject
                        }
                        # if odoo_user:
                        #     task_data['user_ids'] = [(6, 0, odoo_user.ids)]
                        if not check_task:
                            task_data['name'] = '#%d' % st.issue
                            check_task = self.env['project.task'].sudo().create(task_data)
                        else:
                            check_task.write(task_data)

                        user_spent_time = {
                            'date': st.spent_on,
                            'project_id': self.env.ref('bhs_connector_redmine.bh_project_redmine').id,
                            'employee_id': odoo_user.employee_id.id or odoo_emp.id,
                            'task_id': check_task.id,
                            'unit_amount': st.hours,
                            'redmine_activity': st.activity
                        }

                        # Tao timesheet
                        check_timesheet = self.env['account.analytic.line'].sudo().search(
                            [('name', '=', '#%d' % st.id)], limit=1)
                        try:
                            if not check_timesheet:
                                user_spent_time['name'] = '#%d' % st.id
                                self.env['account.analytic.line'].sudo().create(user_spent_time)
                            else:
                                check_timesheet.write(user_spent_time)
                        except Exception as e:
                            print('Error: %s' % e)  # todo: does not work for second company
                # khong co thì add vao list mail de logs
                else:
                    time_entries_no_odoo = redmine.time_entry.filter(user_id=user.id, from_date=from_date_filter,
                                                                     to_date=to_date_filter)
                    if time_entries_no_odoo:
                        users_not_in_odoo.append(user.mail)
                    else:
                        users_not_in_odoo_not_log_time.append(user.mail)
            # xóa spent time có trên redmine mà ko có trên odoo của dự án redmine
            timesheet_odoo_data = self.env['account.analytic.line'].sudo().search(
                [('date', '>=', from_date_filter), ('date', '<=', to_date_filter),
                 ('project_id', '=', self.env.ref('bhs_connector_redmine.bh_project_redmine').id)])
            st_redmine_data = redmine.time_entry.filter(from_date=from_date_filter, to_date=to_date_filter)
            ids_spent_time = [st.id for st in st_redmine_data]
            list_delete = []
            for timesheet in timesheet_odoo_data:
                id_st_odoo = int(timesheet.name.replace("#", ""))
                if id_st_odoo not in ids_spent_time:
                    list_delete.append(timesheet.id)
            if list_delete:
                self.env['account.analytic.line'].sudo().browse(list_delete).unlink()

            # log
            text_logs = "* Cron time (UTC): " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\n"
            text_logs += "* From: " + from_date_filter + " - To: " + to_date_filter + "\n"
            if users_not_in_odoo:
                text_logs += "* List users not in odoo (Have log time): \n" + ("\n".join(users_not_in_odoo)) + "\n"
            if users_not_in_odoo_not_log_time:
                text_logs += "* List users not in odoo (No log time): \n" + ("\n".join(users_not_in_odoo_not_log_time))

            self.env['bh.api.logs'].sudo().create({
                'log_date': datetime.now(),
                'type': 'redmine',
                'logs': text_logs
            })

    def notification_spent_time(self):
        redmine_page = self.env['ir.config_parameter'].sudo().get_param('redmine_page')
        # ngày hôm trước
        noti_date = (date.today() - timedelta(days=1)).isoformat()
        timesheet_odoo_data = self.env['account.analytic.line'].sudo().read_group(
            [('date', '=', noti_date), ('project_id', '=', self.env.ref('bhs_connector_redmine.bh_project_redmine').id)],
        ['date','employee_id','unit_amount'],['employee_id','date:day'])

        for ts in timesheet_odoo_data:
            if ts['unit_amount'] < 7.5:
                odoo_emp = self.env['hr.employee'].sudo().browse(ts['employee_id'][0])
                if odoo_emp:
                    slack_user_configs = odoo_emp.user_id.slack_user_config.filtered(lambda rec: rec.active == True)

                    # có cấu hình nhận thông báo qua slack
                    _logger.info("User: %s" % odoo_emp.user_id.name)
                    if slack_user_configs:
                        for slack_user_config in slack_user_configs:
                            _logger.info("Slack_user_configs: %s" % slack_user_configs)
                            text_slack = _(':speech_balloon: *Thông báo từ Odoo*:')
                            text_slack += _('\nNgày ') + (date.today() - timedelta(days=1)).strftime("%d-%m-%Y")
                            text_slack += _('\nBạn đã log-time trên <'+redmine_page+'|Redmine> ít hơn 8hs! Số giờ bạn đã log là ') + str(ts['unit_amount']) + 'hs'

                            client = slack.WebClient(token=slack_user_config.slack_connector.access_token)
                            client.chat_postMessage(channel=slack_user_config.member_id, text=text_slack)
                    else:
                        _logger.info("Send mail")
                        _logger.info("Email: %s" % odoo_emp.user_id.login if odoo_emp.user_id else odoo_emp.work_email)
                        mail_template = self.env.ref('bhs_connector_redmine.email_template_data_applicant_invite')
                        template_ctx = {
                            'noti_date': (date.today() - timedelta(days=1)).strftime("%d-%m-%Y"),
                            'unit_amount': str(ts['unit_amount']) + 'hs',
                            'redmine_page': redmine_page
                        }
                        body = mail_template._render_field('body_html', odoo_emp.ids, options={'post_process': True},
                                                       add_context=template_ctx)[odoo_emp.id]
                        email_values = {
                            'email_to': odoo_emp.user_id.login if odoo_emp.user_id else odoo_emp.work_email,
                            'body_html': body,
                        }
                        mail_template.send_mail(self.id, force_send=True, email_values=email_values)

    def notification_missing_log_time(self, days=1, access_token='', id_channel=False):
        # ngày hôm trước
        yesterday = (date.today() - timedelta(days=days))
        noti_date = yesterday.isoformat()

        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)

        public_holiday = self.env['resource.calendar.leaves'].sudo().search([])
        holiday = []
        for rec in public_holiday:
            if rec.date_from.year == yesterday.year and not rec.calendar_id.id:
                for d in daterange(rec.date_from.date(), rec.date_to.date() + timedelta(1)):
                    holiday.append(d)

        if yesterday.weekday() > 4 or yesterday in holiday:#neu ngay check la ngay t7, cn hoac la public holiday thi bo qua ko thong bao nua
            return False

        departments = self.env['hr.department'].sudo().search([('need_logwork', '=', True)])
        notification_all = ''

        for department in departments:
            bx_detail = ''
            timesheet_bugfix_odoo_data = self.env['account.analytic.line'].sudo().read_group(
                [('date', '=', noti_date), ('department_id', '=', department.id), ('redmine_activity','=','Bug-Fix')],
                ['date', 'department_id', 'unit_amount'], ['department_id', 'date:day'])
            if timesheet_bugfix_odoo_data:
                bx_detail += '\nTotal Bug-Fix: %0.2f' % (timesheet_bugfix_odoo_data[0]['unit_amount'])
            bx_employees = self.env['hr.employee'].sudo().search([('department_id', '=', department.id)])
            for employee in bx_employees:
                timesheet_odoo_data = self.env['account.analytic.line'].sudo().read_group(
                    [('date', '=', noti_date), ('employee_id', '=', employee.id)],
                    ['date', 'employee_id', 'unit_amount'], ['employee_id', 'date:day'])
                if not timesheet_odoo_data:
                    bx_detail += '\n\t- %s: Not logwork' % (employee.name)
                else:
                    if timesheet_odoo_data[0]['unit_amount'] < 7.5:
                        bx_detail += '\n\t- %s: Logwork %0.2f hrs' % (employee.name, timesheet_odoo_data[0]['unit_amount'])
                    timesheet_bugfix_odoo_data = self.env['account.analytic.line'].sudo().read_group(
                        [('date', '=', noti_date), ('employee_id', '=', employee.id), ('redmine_activity','=','Bug-Fix')],
                        ['date', 'employee_id', 'unit_amount','redmine_activity'], ['redmine_activity', 'date:day'])
                    if timesheet_bugfix_odoo_data:
                        bx_detail += '\n\t- %s: Bug-Fix %0.2f hrs' % (employee.name, timesheet_bugfix_odoo_data[0]['unit_amount'])
            if bx_detail != '':
                notification_all += ('\n\n*** %s:' % department.name) + bx_detail

        # print(notification_all)
        if notification_all != '':
            text_slack = _(':speech_balloon: *Thông báo logwork*:')
            days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
            text_slack += _('\n %s, Ngày %s') % (days[yesterday.weekday()], yesterday.strftime("%d-%m-%Y"))
            text_slack += notification_all
            # print(text_slack)
            try:
                client = slack.WebClient(token=access_token)
                client.chat_postMessage(channel=id_channel, text=text_slack)
            except Exception as e:
                _logger.warning(
                    f'Fail to send message to slack: {str(e)}')

