import odoo
from odoo import _
import logging
from odoo import models, fields, api
from datetime import date, datetime, timedelta
from redminelib import Redmine

import slack, html
from htmlslacker import HTMLSlacker

_logger = logging.getLogger(__name__)

class HRDepartment(models.Model):
    _inherit = 'hr.department'

    need_logwork = fields.Boolean('Need Logwork', default=True)
