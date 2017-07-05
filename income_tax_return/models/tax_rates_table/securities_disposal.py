# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# 
# 
# ---------------------------------------------------------------------
from openerp import models, fields, api

class securities_disposal(models.Model):
	_name       = 'securities.disposal'

	period      	= fields.Char()
	y2015        	= fields.Float(string="Tax Year 2015")
	y2016 			= fields.Float(string="Tax Year 2016")
	y2017   		= fields.Float(string="Tax Year 2017")

	securities_disposal_id = fields.Many2one('tax_rates_table.tax_rates_table',
        ondelete='cascade', string="Securities Disposal", required=True)