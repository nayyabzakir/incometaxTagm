# -*- coding: utf-8 -*-
###############################################################
########### Fields for WorkBook "Income Under FTR" ##########
###############################################################

from openerp import models, fields, api

class income_under_ftr(models.Model):
	_name = 'income.under.ftr'

	description = fields.Char()
	amount      = fields.Float()
	rate        = fields.Float()
	tax         = fields.Float()

	@api.onchange('amount','rate')
	def _onchange_ftr_vals(self):
		self.tax = self.amount * self.rate

	income_under_ftr_id = fields.Many2one('tax.computation',ondelete='cascade', required=True)


	receipts_id = fields.Many2one('receipts',
        ondelete='cascade', string="Receipts")