# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    config_redmine_page = fields.Char(string="Redmine page", config_parameter="redmine_page")
    config_redmine_api_key = fields.Char(string="Redmine API Key", config_parameter="redmine_api_key")
