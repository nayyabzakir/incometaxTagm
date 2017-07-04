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
	receipt_type = fields.Selection([
		('ncr', 'Non Cash'),
		('income', 'Income'),
		('liability', 'Liability'),
		('capital_gain', 'Capital Gain'),
		('asset', 'Asset'),
		('sal', 'Salary'),
		('bus', 'Business'),
		('property', 'Property'),
		('oth_sour', 'Other Sources'),
		('cgt', 'CGT'),
		('foreign_remit', 'Foreign Remittance'),
		('arg_in', 'Agricultural Income'),
		])
	@api.onchange('amount','rate')
	def _onchange_ftr_vals(self):
		self.tax = self.amount * self.rate

	income_under_ftr_id = fields.Many2one('tax.computation',ondelete='cascade')


	receipts_id = fields.Many2one('receipts',
        ondelete='cascade', string="Receipts")