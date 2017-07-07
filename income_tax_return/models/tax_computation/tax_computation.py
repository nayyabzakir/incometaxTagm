#--------------------------------------------------------------------------------
#
#
#--------------------------------------------------------------------------------

from openerp import models, fields, api
from openerp.exceptions import Warning
class tax_computation(models.Model):
	_name = 'tax.computation'

	client_name             = fields.Many2one('res.partner','Client Name', required=True)
	tax_year                = fields.Many2one('account.fiscalyear', 'Tax Year', required=True)
	group                   = fields.Many2one('res.partner')
	tax_computation 		= fields.Many2one('tax.computation')
	_rec_name 			    = 'custom_seq'
	custom_seq      		= fields.Char(string="Name")
	comparative_id 			= fields.Many2one('comparative.wealth', string = 'Comparative Wealth')
	last_year_computation   = fields.Many2one('tax.computation')
	income_under_ntr        = fields.Float(string="Income under NTR")
	exempt_income           = fields.Float(string="Exempt Income ")
	deductible_allowance    = fields.Float(string="Deductible Allowance")
	taxable_income          = fields.Float(string="Taxable Income")
	tax_rate                = fields.Float(string="Rate of Tax")
	fixed_tax               = fields.Float(string="Fixed Tax")
	tax_liability           = fields.Float(string="Tax Liability")
	portion_of_minimum_tax  = fields.Float(string="Portion of Minimum Tax")
	payable_tax             = fields.Float(string="Total Tax Payable")
	tax_adjust              = fields.Float(string="Tax deducted Adjustable")
	tax_deduct_min          = fields.Float(string="Tax deducted Minimum")
	total_tax               = fields.Float(string="Total Tax")
	tax_credits             = fields.Float(string="Tax Credits")
	refund_adjust           = fields.Float(string="Refund Adjustment")
	tax_ratio               = fields.Float(string="Tax Payable/ (Refundable)")
	rebate                  = fields.Float()
	admitted_tax            = fields.Float(string="Admitted Tax")
	income_under_ftr        = fields.Float(string="Income under FTR")
	tax_deduct              = fields.Float(string="Tax deducted")
	tax_computation_ntr_id        = fields.One2many('income.under.ntr', 'income_under_ntr_id')
	tax_computation_deductible_id = fields.One2many('deductible.allowance', 'deductible_allowance_id')
	tax_credits_id                = fields.One2many('tax.credits', 'tax_credits_id')
	tax_rebate_id                 = fields.One2many('income.rebate', 'income_rebate_id')
	tax_computation_ftr_id        = fields.One2many('income.under.ftr', 'income_under_ftr_id')
	tax_deduct_link_id            = fields.One2many('tax.deduct', 'tax_deduct_id')
	tax_computation_exempt_id     = fields.One2many('income.under.exempt', 'income_under_exempt_id')
	pnl_computation           = fields.One2many('pnl.computation.workbook', 'tax_computation_id')
	

	tc_salary           = fields.Float(string="Salary")
	tc_business         = fields.Float(string="Business")
	tc_property         = fields.Float(string="Property")
	tc_other_sources    = fields.Float(string="Other Sources")
	tc_cgt           	= fields.Float(string="CGT")
	tc_for_remit        = fields.Float(string="Foreign Remittance")
	tc_arg_in           = fields.Float(string="Agricultural Income")
	tc_total_income     = fields.Float(string="Total Income")
	tc_less_exempt		= fields.Float(string="Less Exempt")
	tc_less_ftr			= fields.Float(string="Less FTR")
	tc_ftr_exempt_diff	= fields.Float(string="Total")
	tc_less_ded_allowed	= fields.Float(string="Less Deductable Allowance ")
	tc_fe_ded_diff		= fields.Float(string="Total")
	tc_less_cap_gain    = fields.Float(string="Less Capital Gain")
	tc_less_property    = fields.Float(string="Less Property")
	tc_ntr 				= fields.Float(string="NTR")
	tc_tax_liabilty		= fields.Float(string="Tax Liability Under NTR")
	tc_tax_already_ded	= fields.Float(string="Tax Already Deducted")
	tc_tax_pay_refund	= fields.Float(string="Net Tax Payable / (Refundable)")
	tc_tax_charge_ftr	= fields.Float(string="Tax Chargable under FTR ")
	tc_tax_deduct_ftr	= fields.Float(string="Tax Deducted under FTR ")
	tc_income_from_prp	= fields.Float(string="Income From Property ")
	tc_taxable_ifd		= fields.Float(string="Taxable Income From Property")
	tc_tax_liability_ifd= fields.Float(string="Tax Liability From Property")
	tc_capital_gain	    = fields.Float(string="Capital Gain")
	tc_exmt_cg			= fields.Float(string="Exempt Capital Gain ")
	tc_balnc_taxable	= fields.Float(string="Balance Taxable")
	tc_tax_pay_cg		= fields.Float(string="Tax Payable on Capital Gain")
	tc_tax_paid_cg		= fields.Float(string="Tax Paid on Capital Gain")
	tc_ttl_ntr			= fields.Float(string="NTR")
	tc_ttl_ftr			= fields.Float(string="FTR")
	tc_ttl_sbi			= fields.Float(string="Separate Block Income")
	tc_total_tax_lib	= fields.Float(string="Total Tax Liability")
	tc_ttd_ntr			= fields.Float(string="NTR")
	tc_ttd_ftr			= fields.Float(string="FTR")
	tc_ttd_sbi			= fields.Float(string="Separate Block Income")
	tc_total_tax_ded	= fields.Float(string="Total Tax Deducted")
	tc_final_pay_refund	= fields.Float(string="Net Tax Payable / (Refundable)")

	# tc_sca 				= fields.Boolean(string="Senior Citizen Allowance")
	# tc_fta 				= fields.Boolean(string="Full time Teacher Allowance")
	# tc_ftc 				= fields.Boolean(string="Foreign Tax Credit")
	# tc_donations		= fields.Boolean(string="Donations")
	# tc_inv_shares		= fields.Boolean(string="Investment in Shares")
	# tc_inv_hi			= fields.Boolean(string="Investment on Health Insurance")
	# tc_capf				= fields.Boolean(string="Contribution to approved pension fund")
	# tc_rusta			= fields.Boolean(string="Registration under Sales Tax Act ")
	# tc_emp_gen			= fields.Boolean(string="Employment Generation")
	# tc_inv_plnmach		= fields.Boolean(string="Investment in Plant and Machinery")
	# tc_enlistment		= fields.Boolean(string="Enlistment")
	# tc_ind_eqtinv		= fields.Boolean(string="Industrial underetakings [Equity Investment]")
	# tc_ind_plnmach		= fields.Boolean(string="Industrial underetakings [Plant and Machinery]")

	tax_cr_tree_ids		= fields.Many2many('tax.credits.tree')



	@api.model
	def create(self, vals):
		recs = self.env['tax.computation'].search([('client_name','=',vals['client_name']),('tax_year','=',vals['tax_year'])])
		if recs:
			raise Warning("Multiple years for same client cant be done..!")
		return super(tax_computation, self).create(vals)

	@api.onchange('tax_computation_ntr_id')
	def _onchange_ntr_id(self):
		self.income_under_ntr = sum(line.amount for line in self.tax_computation_ntr_id if line.tax_type!='exempt')

	@api.onchange('tax_computation_deductible_id')
	def _onchange_deductible_id(self):
		self.deductible_allowance = sum(line.tax for line in self.tax_computation_deductible_id)

	@api.onchange('tax_rebate_id')
	def _onchange_rebate_id(self):
		self.rebate = sum(line.tax for line in self.tax_rebate_id)

	@api.onchange('tax_credits_id')
	def _onchange_credits_id(self):
		self.tax_credits = sum(line.tax for line in self.tax_credits_id)

	@api.onchange('tax_computation_ftr_id')
	def _onchange_ftr_id(self):
		self.income_under_ftr = sum(line.amount for line in self.tax_computation_ftr_id)
		self.tax_deduct = sum(line.tax for line in self.tax_computation_ftr_id)

	@api.onchange('tax_deduct_link_id')
	def _onchange_tax_deduct(self):
		self.tax_adjust = sum(line.amount for line in self.tax_deduct_link_id if line.tax_type=='adjustable')
		self.tax_deduct_min = sum(line.amount for line in self.tax_deduct_link_id if line.tax_type=='minimum')

		@api.onchange('tc_salary','tc_business','tc_property','tc_other_sources','tc_cgt','tc_for_remit','tc_arg_in')
		def _onchange_sub_types(self):
			self.tc_total_income=self.tc_salary+self.tc_business+self.tc_property+self.tc_other_sources+self.tc_cgt+self.tc_for_remit+self.tc_arg_in
			
		@api.onchange('tc_total_income','tc_less_exempt','tc_less_ftr')
		def _onchange_tc_total_income(self):
			self.tc_ntr = self.tc_total_income - (self.tc_less_exempt + self.tc_less_ftr)


	@api.onchange('income_under_ntr','rebate','tax_rate','deductible_allowance','tax_credits','fixed_tax','portion_of_minimum_tax','tax_adjust','tax_deduct_min','refund_adjust')
	def onchange_assesment_form_field(self):
		self.taxable_income = self.income_under_ntr - self.deductible_allowance
		self.tax_liability  = (self.taxable_income * self.tax_rate) + self.fixed_tax
		self.total_tax      = self.payable_tax - self.tax_adjust
		self.total_tax      = self.total_tax - self.tax_deduct_min
		self.tax_ratio      = self.total_tax - self.refund_adjust - self.tax_credits
		self.admitted_tax   = self.tax_ratio - self.rebate
		if self.portion_of_minimum_tax < self.tax_deduct_min:
			self.payable_tax    = self.tax_liability - self.portion_of_minimum_tax + self.tax_deduct_min
		elif self.portion_of_minimum_tax > self.tax_deduct_min:
			self.payable_tax = self.tax_liability

	@api.multi
	def update_computation(self):
		self.tax_computation_ntr_id.unlink()
		self.tax_computation_ftr_id.unlink()
		self.tax_deduct_link_id.unlink()
		required_class = self.env['comparative.wealth'].search([('name','=',self.client_name.id)])

		self.income_under_ntr = sum(line.amount for line in self.tax_computation_ntr_id if line.tax_type != 'exempt')
		self.exempt_income = sum(line.amount for line in self.tax_computation_ntr_id if line.tax_type == 'exempt')
		self.tax_deduct = sum(line.amount for line in self.tax_deduct_link_id if line.tax_type == 'tax_ftr')
		self.income_under_ftr = sum(line.amount for line in self.tax_computation_ftr_id)
		self.tax_adjust = sum(line.amount for line in self.tax_deduct_link_id if line.tax_type == 'adjustable')
		self.tax_deduct_min = sum(line.amount for line in self.tax_deduct_link_id if line.tax_type == 'minimum')
		self.taxable_income = self.income_under_ntr - self.deductible_allowance
		self.payable_tax = self.tax_liability + self.portion_of_minimum_tax
		self.createIncomeUNTR()
		self.createIncomeUFTR()
		self.createTaxDeducted()
		self.createIncomeUExempt()
		self.createDedAllowance()
		self.getTaxCompDetails()
		self.getBusinessProfit()
		self.computeTaxCredit()


	def getTaxCompDetails(self):
		self.tc_salary =  sum(line.amount for line in self.tax_computation_ntr_id if line.receipt_type =='sal') + sum(line.amount for line in self.tax_computation_ftr_id if line.receipt_type =='sal') + sum(line.amount for line in self.tax_computation_exempt_id if line.sub_type =='sal')
		self.tc_business =  sum(line.amount for line in self.tax_computation_ntr_id if line.receipt_type =='bus') + sum(line.amount for line in self.tax_computation_ftr_id if line.receipt_type =='bus') + sum(line.amount for line in self.tax_computation_exempt_id if line.sub_type =='bus')
		self.tc_property =  sum(line.amount for line in self.tax_computation_ntr_id if line.receipt_type =='property') + sum(line.amount for line in self.tax_computation_ftr_id if line.receipt_type =='property') + sum(line.amount for line in self.tax_computation_exempt_id if line.sub_type =='property')
		self.tc_less_property =  sum(line.amount for line in self.tax_computation_ntr_id if line.receipt_type =='property') + sum(line.amount for line in self.tax_computation_ftr_id if line.receipt_type =='property') + sum(line.amount for line in self.tax_computation_exempt_id if line.sub_type =='property')
		self.tc_other_sources =  sum(line.amount for line in self.tax_computation_ntr_id if line.receipt_type =='oth_sour') + sum(line.amount for line in self.tax_computation_ftr_id if line.receipt_type =='oth_sour') + sum(line.amount for line in self.tax_computation_exempt_id if line.sub_type =='oth_sour')
		self.tc_cgt =  sum(line.amount for line in self.tax_computation_ntr_id if line.receipt_type =='cgt') + sum(line.amount for line in self.tax_computation_ftr_id if line.receipt_type =='cgt') + sum(line.amount for line in self.tax_computation_exempt_id if line.sub_type =='cgt')
		self.tc_for_remit =  sum(line.amount for line in self.tax_computation_ntr_id if line.receipt_type =='foreign_remit') + sum(line.amount for line in self.tax_computation_ftr_id if line.receipt_type =='foreign_remit') + sum(line.amount for line in self.tax_computation_exempt_id if line.sub_type =='foreign_remit')
		self.tc_arg_in =  sum(line.amount for line in self.tax_computation_ntr_id if line.receipt_type =='arg_in') + sum(line.amount for line in self.tax_computation_ftr_id if line.receipt_type =='arg_in') + sum(line.amount for line in self.tax_computation_exempt_id if line.sub_type =='arg_in')
		self.tc_total_income=self.tc_salary+self.tc_business+self.tc_property+self.tc_other_sources+self.tc_cgt+self.tc_for_remit+self.tc_arg_in
		self.tc_less_exempt =   sum(line.amount for line in self.tax_computation_exempt_id)
		self.tc_less_ftr =  sum(line.amount for line in self.tax_computation_ftr_id)
		self.tc_ntr = self.tc_total_income - (self.tc_less_exempt + self.tc_less_ftr) - self.tc_less_cap_gain - self.tc_less_property
		self.tc_tax_already_ded =  sum(line.amount for line in self.tax_deduct_link_id if line.tax_type =='adjustable')
		self.tc_tax_pay_refund = self.tc_tax_liabilty - self.tc_tax_already_ded
		self.tc_less_ded_allowed =  sum(line.ded_allowed for line in self.tax_computation_deductible_id)
		self.tc_ftr_exempt_diff =  self.tc_total_income - self.tc_less_exempt - self.tc_less_ftr
		self.tc_fe_ded_diff =  self.tc_ftr_exempt_diff - self.tc_less_ded_allowed

	def computeTaxCredit(self):
		if self.tax_cr_tree_ids:
			for line in self.tax_cr_tree_ids:
				tc_record = self.tax_credits_id.search([('description','=',line.name)])
				if tc_record:
					if line.rate != 0:
						tc_record.amount = self.tc_tax_liabilty * line.rate
				else:
					self.tax_credits_id.create({
						'description' : line.name,
						'amount' : self.tc_tax_liabilty * line.rate,
						'tax_credits_id' : self.id,
						})

	def getBusinessProfit(self):
		if self.pnl_computation:
			for line in self.pnl_computation:
				################### Records Creation For Income Under NTR #################
				if line.business_name.name.business_type == 'sp':
					ntr_id = self.tax_computation_ntr_id.search([('pnl_id','=',line.id)])
					if not ntr_id:
						self.tax_computation_ntr_id.create({
							'description' : "Profit for "+line.business_name.name.name,
							'receipt_type' : "bus",
							'sub_tax_type' : 'nor',
							'tax_type' : 'ntr',
							'income_under_ntr_id': self.id,
							'amount' : line.business_name.tax_profit,
							'pnl_id' : line.id
							})
					else:
						ntr_id.description = "Profit for "+line.business_name.name.name
						ntr_id.amount = line.business_name.tax_profit
					################### Records Creation For Income Under FTR #################
					ftr_id = self.tax_computation_ftr_id.search([('pnl_id','=',line.id)])
					if not ftr_id:
						self.tax_computation_ftr_id.create({
							'description' : "Profit for "+line.business_name.name.name,
							'receipt_type' : "bus",
							'income_under_ftr_id': self.id,
							'amount' : line.business_name.ftr_tax_profit,
							'pnl_id' : line.id
							})
					else:
						ftr_id.description = "Profit for "+line.business_name.name.name
						ftr_id.amount = line.business_name.ftr_tax_profit
				################### Records Creation For Exempt  Income #################
				elif line.business_name.name.business_type == 'aop':
					exempt_id = self.tax_computation_exempt_id.search([('pnl_id','=',line.id)])
					if not exempt_id:
						self.tax_computation_exempt_id.create({
							'description' : "Profit for "+line.business_name.name.name,
							'sub_type' : "bus",
							'income_under_exempt_id': self.id,
							'amount' : line.business_name.tax_profit,
							'pnl_id' : line.id
							})
					else:
						exempt_id.description = "Profit for "+line.business_name.name.name
						exempt_id.amount = line.business_name.tax_profit



	def createIncomeUNTR(self):
		required_class = self.env['comparative.wealth'].search([('name','=',self.client_name.id)])

		self.tax_computation_ntr_id.unlink()
		year = 'y'+str(self.tax_year.code)
		for line in required_class.cash_receipts_ids:
			if line.tax_type == 'ntr':
				new_ntr_id = self.tax_computation_ntr_id.create({
					'description' : line.description,
					'receipt_type' : line.sub_type,
					'receipts_id': line.id,
					'sub_tax_type' : 'nor',
					'income_under_ntr_id': self.id
					})
				self.env.cr.execute("UPDATE income_under_ntr b SET    amount = a."+year+" FROM   receipts a WHERE  b.receipts_id = a.id and b.id = "+str(new_ntr_id.id)+"")
			elif line.tax_type == 'minimum':
				new_min_id = self.tax_computation_ntr_id.create({
					'description' : line.description,
					'receipt_type' : line.sub_type,
					'receipts_id': line.id,
					'sub_tax_type' : 'min',
					'income_under_ntr_id' : self.id,
					})
				self.env.cr.execute("UPDATE income_under_ntr b SET    amount = a."+year+" FROM   receipts a WHERE  b.receipts_id = a.id and b.id = "+str(new_min_id.id)+"")

	def createIncomeUFTR(self):
		required_class = self.env['comparative.wealth'].search([('name','=',self.client_name.id)])

		self.tax_computation_ftr_id.unlink()
		year = 'y'+str(self.tax_year.code)
		for line in required_class.cash_receipts_ids:
			if line.tax_type == 'ftr':
				new_ftr_id = self.tax_computation_ftr_id.create({
					'description' : line.description,
					'receipts_id': line.id,
					'receipt_type' : line.sub_type,
					'income_under_ftr_id': self.id,
					})
				self.env.cr.execute("UPDATE income_under_ftr b SET    amount = a."+year+" FROM   receipts a WHERE  b.receipts_id = a.id and b.id = "+str(new_ftr_id.id)+"")


	def createIncomeUExempt(self):
		required_class = self.env['comparative.wealth'].search([('name','=',self.client_name.id)])

		self.tax_computation_exempt_id.unlink()
		year = 'y'+str(self.tax_year.code)
		for line in required_class.cash_receipts_ids:
			if line.tax_type == 'exempt':
				new_exempt_id = self.tax_computation_exempt_id.create({
					'description' : line.description,
					'receipts_id': line.id,
					'sub_type': line.sub_type,
					'income_under_exempt_id': self.id,
					})
				self.env.cr.execute("UPDATE income_under_exempt b SET    amount = a."+year+" FROM   receipts a WHERE  b.receipts_id = a.id and b.id = "+str(new_exempt_id.id)+"")


	def createTaxDeducted(self):
		required_class = self.env['comparative.wealth'].search([('name','=',self.client_name.id)])

		self.tax_deduct_link_id.unlink()
		year = 'y'+str(self.tax_year.code)
		for line in required_class.cash_payments_ids:
			if line.tax_type:
				new_taxded_id = self.tax_deduct_link_id.create({
					'description' : line.description,
					'payments_id': line.id,
					'tax_deduct_id': self.id,
					'tax_type':line.tax_type,
					})
				self.env.cr.execute("UPDATE tax_deduct b SET    amount = a."+year+" FROM   payments a WHERE  b.payments_id = a.id and b.id = "+str(new_taxded_id.id)+"")


	def createDedAllowance(self):
		required_class = self.env['comparative.wealth'].search([('name','=',self.client_name.id)])

		self.tax_computation_deductible_id.unlink()
		year = 'y'+str(self.tax_year.code)
		for line in required_class.cash_payments_ids.search([('receipt_type','=','ded_all')]):
			print line
			self.tax_computation_deductible_id.create({
				'description' : line.description,
				'deductible_allowance_id': self.id,
				'deductible_allowance_ids': line.deductible_allowance_ids.id,
				'payment_id': line.id,
				})
			self.env.cr.execute("UPDATE deductible_allowance b SET    amount = a."+year+" , ded_allowed= a."+year+"  FROM   payments a WHERE  b.payment_id = a.id")


	@api.multi
	def get_tax_rate(self):
		business_income =  sum(line.amount for line in self.tax_computation_ntr_id if line.tax_type!='exempt' and line.tax_type!='salary')
		salary_income =  sum(line.amount for line in self.tax_computation_ntr_id if line.tax_type =='salary')
		if business_income > salary_income:
			required_class = self.env['tax_rates_table.tax_rates_table'].search([('tax_year','=',self.tax_year.id)])
			tax_rate_book = required_class.business_rates_table_ids
			for x in tax_rate_book:
				if x.amount_from <= self.taxable_income <= x.amount_to:
					taxable_amount = self.taxable_income - x.amount_from
					tax_amount = taxable_amount * x.rate_of_tax
					self.tax_rate = (tax_amount / self.taxable_income) / 100
					self.fixed_tax = x.fixed_tax_amount
					self.tax_liability = self.taxable_income * self.tax_rate + self.fixed_tax
		else:
			required_class = self.env['tax_rates_table.tax_rates_table'].search([('tax_year','=',self.tax_year.id)])
			tax_rate_book = required_class.salaried_rates_table_ids
			for x in tax_rate_book:
				if x.amount_from <= self.taxable_income <= x.amount_to:
					taxable_amount = self.taxable_income - x.amount_from
					tax_amount = taxable_amount * x.rate_of_tax
					self.tax_rate = (tax_amount / self.taxable_income) / 100
					self.fixed_tax = x.fixed_tax_amount
					self.tax_liability = self.taxable_income * self.tax_rate + self.fixed_tax

	@api.multi
	def virtual_tax_minimum(self):
		business_income =  sum(line.amount for line in self.tax_computation_ntr_id if line.tax_type!='exempt' and line.tax_type!='salary')
		salary_income =  sum(line.amount for line in self.tax_computation_ntr_id if line.tax_type =='salary')
		virtual_income = sum(line.amount for line in self.tax_computation_ntr_id if line.tax_type !='minimum')
		if business_income > salary_income:
			required_class = self.env['tax_rates_table.tax_rates_table'].search([('tax_year','=',self.tax_year.id)])
			tax_rate_book = required_class.business_rates_table_ids
			for x in tax_rate_book:
				if x.amount_from <= virtual_income <= x.amount_to:
					taxable_amount = virtual_income - x.amount_from
					tax_amount = taxable_amount * x.rate_of_tax/100
					virtual_liability = tax_amount + x.fixed_tax_amount
					self.portion_of_minimum_tax = self.tax_liability - virtual_liability
					if self.portion_of_minimum_tax > self.tax_deduct_min:
						self.payable_tax = self.tax_liability
					elif self.portion_of_minimum_tax < self.tax_deduct_min:
						self.payable_tax = self.tax_liability - self.portion_of_minimum_tax + self.tax_deduct_min
					else:
						return
		else:
			required_class = self.env['tax_rates_table.tax_rates_table'].search([('tax_year','=',self.tax_year.id)])
			tax_rate_book = required_class.salaried_rates_table_ids
			for x in tax_rate_book:
				if x.amount_from <= virtual_income <= x.amount_to:
					taxable_amount = virtual_income - x.amount_from
					tax_amount = taxable_amount * x.rate_of_tax/100
					virtual_liability = tax_amount + x.fixed_tax_amount
					self.portion_of_minimum_tax = self.tax_liability - virtual_liability

	@api.onchange('client_name','tax_year')
	def _get_comparative(self):
		required_class = self.env['comparative.wealth'].search([('name.id','=',self.client_name.id)])
		self.comparative_id = required_class.id
		client_name_seq = str(self.client_name.name)
		tax_year_seq    = str(self.tax_year.code)
		self.custom_seq = client_name_seq + " / " + tax_year_seq


	@api.multi
	def update_tax_depriciation(self):
		if self.pnl_computation:
			for line in self.pnl_computation:
				for sheet in self.comparative_id.balance_sheet_workbook_ids:
					for asset in sheet.business.balance_sheet_id:
						if asset.selection_type == "noncurrent":
							if line.business_name.id == sheet.business.tax_comp_bus.id:
								balance_sheet_rec =  line.business_name.accounting_tax_ids.search([('bal_sheet_asset_id','=',asset.id)])
								# balance_sheet_rec.unlink()
								if not balance_sheet_rec:
									line.business_name.accounting_tax_ids.create({
											'desc' : asset.description,
											'bal_sheet_asset_id' : asset.id,
											'accounting_tax_id' : line.business_name.id
											})
									if self.tax_year:
										year = 'y'+str(int(self.tax_year.name)-1)
										self.env.cr.execute("UPDATE pnl_tax_depreciation b SET    wdv_bf = a."+str(year)+" FROM   balance_sheet_sub_sub_balance_sheet_sub_sub a WHERE  b.bal_sheet_asset_id = a.id")
								else:
									if self.tax_year:
										year = 'y'+str(int(self.tax_year.name)-1)
										self.env.cr.execute("UPDATE pnl_tax_depreciation b SET    wdv_bf = a."+str(year)+" FROM   balance_sheet_sub_sub_balance_sheet_sub_sub a WHERE  b.bal_sheet_asset_id = a.id")
		# Setting Current Year Value as wdv_cf (closing) of previous Year
		if self.tax_year:
			year = 'y'+str(self.tax_year.name)
			for pl in self.pnl_computation:
				for td in pl.business_name.accounting_tax_ids:
					for bls in self.comparative_id.balance_sheet_workbook_ids:
						for ast in bls.business.balance_sheet_id:
							if td.desc == ast.description:
								self.env.cr.execute("UPDATE balance_sheet_sub_sub_balance_sheet_sub_sub b SET    "+str(year)+" = a.wdv_cf FROM   pnl_tax_depreciation a WHERE  b.id = a.bal_sheet_asset_id")


		# Getting Accounting Depriciation Records from previous year
		# Previous Year WDV(CF)(Closing) is = Current Year WDV(BF)(Opening)
		for line in self.pnl_computation:
			year = str(int(self.tax_year.name)-1)
			tax_comp_recs = self.env['tax.computation'].search([('client_name.id','=',self.client_name.id),('tax_year.name','=',year)])
			if tax_comp_recs:
				for tcr in tax_comp_recs.pnl_computation:
					for ad in tcr.business_name.accounting_depreciation_ids:
						act_dep_recs = line.business_name.accounting_depreciation_ids.search([('desc','=',ad.desc),('accounting_depreciation_id','=',line.business_name.id)])
						if not act_dep_recs:
							line.business_name.accounting_depreciation_ids.create({
															'desc' : ad.desc,
															'rate' : ad.rate,
															'wdv_bf' : ad.wdv_cf,
															'depreciation' : ad.wdv_cf * ad.rate,
															'wdv_cf' : ad.wdv_cf - (ad.wdv_cf * ad.rate),
															'accounting_depreciation_id' : line.business_name.id
															})
						else:
							act_dep_recs.wdv_bf = ad.wdv_cf
							act_dep_recs.depreciation = (act_dep_recs.wdv_bf + (act_dep_recs.addition_new * (act_dep_recs.month_use / 12)) - (act_dep_recs.deletion * (act_dep_recs.month_use / 12))) * act_dep_recs.rate
