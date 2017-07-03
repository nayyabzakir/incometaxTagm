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
	# total_sale              = fields.Float(string="Total Sales")
	# sale_under_ntr          = fields.Float(string="NTR Sales")
	# sale_under_ftr          = fields.Float(string="FTR/Exempt Sales")
	# ntr_income              = fields.Float(string="NTR Revenue")
	# purchases               = fields.Float(string="Purchases")
	# opening                 = fields.Float(string="Add: Opening")
	# closing                 = fields.Float(string="Less: Closing")
	# cost_of_sales			= fields.Float(string="Cost of Sales")
	# gross_profit			= fields.Float(string="Gross Profit")
	# ntr_expense             = fields.Float(string="NTR Expense")
	# ntr_profit_Loss         = fields.Float(string="NTR Profit/Loss")
	# accounting_depreciation = fields.Float(string="Acc Depreciation")
	# inadmissible_expenses   = fields.Float(string="In admissible Expenses")
	# tax_depreciation	    = fields.Float(string="Tax Depreciation")
	# tax_profit              = fields.Float(string="Tax Profit")
	income_under_ftr        = fields.Float(string="Income under FTR")
	tax_deduct              = fields.Float(string="Tax deducted")
	# description             = fields.Text()
	# amount                  = fields.Float()

	tax_computation_ntr_id        = fields.One2many('income.under.ntr', 'income_under_ntr_id')
	tax_computation_deductible_id = fields.One2many('deductible.allowance', 'deductible_allowance_id')
	tax_credits_id                = fields.One2many('tax.credits', 'tax_credits_id')
	tax_rebate_id                 = fields.One2many('income.rebate', 'income_rebate_id')
	tax_computation_ftr_id        = fields.One2many('income.under.ftr', 'income_under_ftr_id')
	tax_deduct_link_id            = fields.One2many('tax.deduct', 'tax_deduct_id')
	# profit_loss_link_id           = fields.One2many('profit_loss.profit_loss', 'profit_loss_id')

	pnl_computation           = fields.One2many('pnl.computation.workbook', 'tax_computation_id')


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

		for y in self:
			# for x in required_class.wealth_reconciliation_income_ids:
			# 	dic = {
			# 	x.y2005 : '2005',
			# 	x.y2006 : '2006',
			# 	x.y2007 : '2007',
			# 	x.y2008 : '2008',
			# 	x.y2009 : '2009',
			# 	x.y2010 : '2010',
			# 	x.y2011 : '2011',
			# 	x.y2012 : '2012',
			# 	x.y2013 : '2013',
			# 	x.y2014 : '2014',
			# 	x.y2015 : '2015',
			# 	x.y2016 : '2016',
			# 	x.y2017 : '2017',
			# 	x.y2018 : '2018',
			# 	x.y2019 : '2019',
			# 	x.y2020 : '2020',
			# 	}
			# 	for key, value in dic.iteritems():
			# 		if x.receipt_type != 'ftr' and dic[key] == self.tax_year.code:
			# 			y.tax_computation_ntr_id.create({
			# 				'description' : x.description,
			# 				'tax_type':x.receipt_type,
			# 				'amount':key,
			# 				'income_under_ntr_id': y.id,
			# 				})
			# 		elif x.receipt_type == 'ftr' and dic[key] == self.tax_year.code:

			# 			y.tax_computation_ftr_id.create({
			# 				'description' : x.description,
			# 				'amount':key,
			# 				'income_under_ftr_id': y.id,
			# 				})
			# for x in required_class.cash_receipts_ids:
			# 	dic = {
			# 	x.y2005 : '2005',
			# 	x.y2006 : '2006',
			# 	x.y2007 : '2007',
			# 	x.y2008 : '2008',
			# 	x.y2009 : '2009',
			# 	x.y2010 : '2010',
			# 	x.y2011 : '2011',
			# 	x.y2012 : '2012',
			# 	x.y2013 : '2013',
			# 	x.y2014 : '2014',
			# 	x.y2015 : '2015',
			# 	x.y2016 : '2016',
			# 	x.y2017 : '2017',
			# 	x.y2018 : '2018',
			# 	x.y2019 : '2019',
			# 	x.y2020 : '2020',
			# 	}
			# 	for key, value in dic.iteritems():
			# 		y.tax_computation_ntr_id.create({
			# 			'description' : x.description,
			# 			'tax_type':x.tax_type,
			# 			'receipt_type':x.receipt_type,
			# 			'amount':key,
			# 			'income_under_ntr_id': y.id,
			# 			'receipts_id': x.id,
			# 				})
			for x in required_class.wealth_reconciliation_expense_ids:
				dic = {
				x.y2005 : '2005',
				x.y2006 : '2006',
				x.y2007 : '2007',
				x.y2008 : '2008',
				x.y2009 : '2009',
				x.y2010 : '2010',
				x.y2011 : '2011',
				x.y2012 : '2012',
				x.y2013 : '2013',
				x.y2014 : '2014',
				x.y2015 : '2015',
				x.y2016 : '2016',
				x.y2017 : '2017',
				x.y2018 : '2018',
				x.y2019 : '2019',
				x.y2020 : '2020',
				}
				for key, value in dic.iteritems():
					if x.receipt_type != 'expense' and dic[key] == self.tax_year.code:
						y.tax_deduct_link_id.create({
							'description' : x.description,
							'tax_type':x.receipt_type,
							'amount':key,
							'tax_deduct_id': y.id,
							})
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
		self.createDedAllowance()

	def createIncomeUNTR(self):
		required_class = self.env['comparative.wealth'].search([('name','=',self.client_name.id)])

		self.tax_computation_ntr_id.unlink()
		year = 'y'+str(self.tax_year.code)
		for line in required_class.cash_receipts_ids:
			if line.tax_type == 'ntr':
				new_ntr_id = self.tax_computation_ntr_id.create({
					'description' : line.description,
					'receipt_type' : line.receipt_type,
					'receipts_id': line.id,
					'sub_tax_type' : 'nor',
					'income_under_ntr_id': self.id
					})
				self.env.cr.execute("UPDATE income_under_ntr b SET    amount = a."+year+" FROM   receipts a WHERE  b.receipts_id = a.id and b.id = "+str(new_ntr_id.id)+"")
			elif line.tax_type == 'minimum':
				new_min_id = self.tax_computation_ntr_id.create({
					'description' : line.description,
					'receipt_type' : line.receipt_type,
					'receipts_id': line.id,
					'sub_tax_type' : 'min',
					'income_under_ntr_id' : self.id
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
					'income_under_ftr_id': self.id
					})
				self.env.cr.execute("UPDATE income_under_ftr b SET    amount = a."+year+" FROM   receipts a WHERE  b.receipts_id = a.id and b.id = "+str(new_ftr_id.id)+"")

	def createDedAllowance(self):
		required_class = self.env['comparative.wealth'].search([('name','=',self.client_name.id)])

		self.tax_computation_deductible_id.unlink()
		year = 'y'+str(self.tax_year.code)
		for line in required_class.cash_payments_ids.search([('receipt_type','=','ded_all')]):
			print line
			self.tax_computation_deductible_id.create({
				'description' : line.description,
				'deductible_allowance_id': self.id,
				'payment_id': line.id,
				})
			self.env.cr.execute("UPDATE deductible_allowance b SET    amount = a."+year+" FROM   payments a WHERE  b.payment_id = a.id")




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

	# @api.multi
	# def update(self):
	# 	if self.total_sale != 0:
	# 		ntr_ratio = self.sale_under_ntr / self.total_sale
	# 		ftr_ratio = self.sale_under_ftr / self.total_sale

	# 		for x in self.profit_loss_link_id:
	# 			x.ntr =  x.total * ntr_ratio
	# 			x.ftr_exempt =  x.total * ftr_ratio
	# 	self.ntr_income =  sum(line.ntr for line in self.profit_loss_link_id if line.types =='income')
	# 	self.purchases =  sum(line.ntr for line in self.profit_loss_link_id if line.types =='direct_expenses' and line.admissible == 'admissible')
	# 	self.cost_of_sales =  self.purchases + self.opening - self.closing
	# 	self.gross_profit = self.ntr_income - self.cost_of_sales
	# 	self.accounting_depreciation =  sum(line.ntr for line in self.profit_loss_link_id if line.admissible =='depreciation')
	# 	self.ntr_expense =  sum(line.ntr for line in self.profit_loss_link_id if line.types =='indirect_expenses' and line.admissible == 'admissible')
	# 	self.inadmissible_expenses =  sum(line.ntr for line in self.profit_loss_link_id if line.types !='income' and line.admissible == 'in_admissible')
	# 	self.ntr_profit_Loss = self.gross_profit - self.ntr_expense
	# 	self.tax_profit = self.ntr_profit_Loss + self.accounting_depreciation - self.inadmissible_expenses - self.tax_depreciation

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
