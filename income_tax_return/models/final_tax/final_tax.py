# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# 
# 
# ---------------------------------------------------------------------
from openerp import models, fields, api

class final_tax(models.Model):

	_name      		= 'final_tax.final_tax'
	_description 	= "Final Tax"
	_inherit   		= ['mail.thread', 'ir.needaction_mixin']

	name           	= fields.Char()
	rate         	= fields.Float()
	section 		= fields.Char()
	model_name 		= fields.Char(compute="_compute_rec")

	@api.multi
	def _compute_rec(self):
		self.model_name = '%s @  %s %s u/s %s' %(self.name,self.rate,'%',self.section)


	_rec_name = 'model_name'

