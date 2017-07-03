# -*- coding: utf-8 -*-
###############################################################
########### Fields for WorkBook "Deductible Allowance" ##########
###############################################################

from openerp import models, fields, api

class deductible_allowance(models.Model):
	_name = 'deductible.allowance'

	description = fields.Char()
	amount      = fields.Float()
	rate        = fields.Float()
	tax         = fields.Float()

	@api.onchange('amount','rate')
	def _onchange_ftr_vals(self):
		self.tax = self.amount * self.rate

	deductible_allowance_id = fields.Many2one('tax.computation',ondelete='cascade', required=True)
	payment_id = fields.Many2one('payments',
        ondelete='cascade', string="Payments")