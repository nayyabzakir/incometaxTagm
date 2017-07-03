# -*- coding: utf-8 -*-
###############################################################
########### Fields for WorkBook "Tax Deduct" ##########
###############################################################


from openerp import models, fields, api

class tax_deduct(models.Model):
	_name = 'tax.deduct'

	description = fields.Char()
	amount      = fields.Float()
	tax_type    = fields.Selection([
        ('adjustable', 'Adjustable'),
        ('non_adjustable', 'Non Adjustable'),
        ('minimum', 'Minimum'),
		('tax_ftr', 'Tax FTR'),
        ])

	tax_deduct_id = fields.Many2one('tax.computation',
        ondelete='cascade', required=True)