# -*- coding: utf-8 -*-
###############################################################
########### Fields for WorkBook "Deductible Allowance" ##########
###############################################################

from openerp import models, fields, api

class deductible_allowance(models.Model):
	_name = 'deductible.allowance'

	description = fields.Char()
	deductible_allowance_ids = fields.Many2one('deductable.allowance','Dedutable Allowance')
	amount      = fields.Float()
	ded_allowed        = fields.Float()

	deductible_allowance_id = fields.Many2one('tax.computation',ondelete='cascade', required=True)
	payment_id = fields.Many2one('payments',
        ondelete='cascade', string="Payments")