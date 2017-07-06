# -*- coding: utf-8 -*-
###############################################################
########### Fields for WorkBook "Income Under NTR" ##########
###############################################################

from openerp import models, fields, api

class income_under_ntr(models.Model):
	_name = 'income.under.ntr'

	description = fields.Char()
	amount      = fields.Float()
	tax_type    = fields.Selection([
		('ntr', 'NTR'),
		('ftr', 'FTR'),
		('exempt', 'Exempt'),
		('minimum', 'Minimum'),
		])

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
	sub_tax_type    = fields.Selection([
		('nor', 'NTR'),
		('min', 'Minimum'),
		])
	income_under_ntr_id = fields.Many2one('tax.computation',
		ondelete='cascade')

	receipts_id = fields.Many2one('receipts',
        ondelete='cascade', string="Receipts")

	pnl_id = fields.Many2one('pnl.computation',
        ondelete='cascade', string="PNL Computation ID")