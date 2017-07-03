# -*- coding: utf-8 -*-

from openerp import models, fields, api

class CorresPrototype(models.Model):
    _name = "corres.corres.prototype"
    client_name    = fields.Many2one('res.partner','Client Name', required=True)
    section_no     = fields.Char('Section No ',required=True)
    section_des    = fields.Char('Section Description')
    acc_officer    = fields.Many2one('res.partner','Assessing Officer', required=True)
    date_of_notice = fields.Date('Date of Notice',required=True)
    notice_no      = fields.Char('Notice No ',required=True)
    demand_amount  = fields.Float('Demand Amount')
    assigned_to    = fields.Many2one('hr.employee','Assigned To', required=True)
    assessing_authority = fields.Selection([
            ('ito', 'ITO'),
            ('assistant_commissioner', 'Assistant Commissioner'),
            ('deputy_commissioner', 'Deputy Commissioner'),
            ('commissioner', 'Commissioner'),
            ('atir', 'ATIR'),
            ('high_court', 'High Court'),
            ('supreme_court', 'Supreme Court'),
            ])
    rto    = fields.Many2one('rto.rto','RTO', required=True)
    corres_his = fields.One2many('correspondence.history','correspondence_his')
    tax_year = fields.Char('Tax Year')

# Correspondence Class 
class correspondence(models.Model):
    _name = 'correspondence.correspondence'
    _inherit = 'corres.corres.prototype'

    stages = fields.Selection([
            ('order', 'Order'),
            ('first_appeal', 'First Appeal'),
            ('stay', 'Stay'),
            ('sec_appeal', 'Second Appeal'),
            ('ref_to_hc', 'Reference to High Court'),
            ], default="order")

    vv = fields.Char(compute="_compute_rec")
    @api.multi
    def _compute_rec(self):
        self.vv = '(%s) Notice No %s u/s %s for Tax Year %s' %(self.client_name.name,self.notice_no,self.section_no ,self.tax_year)
    _rec_name = 'vv'


# Assessment Class 
class AssessmentCorres(models.Model):
    _name = 'assessment.corres'
    _inherit = 'corres.corres.prototype'

    vv = fields.Char(compute="_compute_rec")
    @api.multi
    def _compute_rec(self):
        self.vv = '(%s) Notice No %s u/s %s for Tax Year %s' %(self.client_name.name,self.notice_no,self.section_no ,self.tax_year)
    _rec_name = 'vv'

# Audit Class 
class AuditCorres(models.Model):
    _name = 'audit.corres'
    _inherit = 'corres.corres.prototype'

    vv = fields.Char(compute="_compute_rec")
    @api.multi
    def _compute_rec(self):
        self.vv = '(%s) Notice No %s u/s %s for Tax Year %s' %(self.client_name.name,self.notice_no,self.section_no ,self.tax_year)
    _rec_name = 'vv'

# Rectification Class 
class RectificationCorres(models.Model):
    _name = 'rectification.corres'
    _inherit = 'corres.corres.prototype'

    vv = fields.Char(compute="_compute_rec")
    @api.multi
    def _compute_rec(self):
        self.vv = '(%s) Notice No %s u/s %s for Tax Year %s' %(self.client_name.name,self.notice_no,self.section_no ,self.tax_year)
    _rec_name = 'vv'

# Recovery Class 
class RecoveryCorres(models.Model):
    _name = 'recovery.corres'
    _inherit = 'corres.corres.prototype'

    vv = fields.Char(compute="_compute_rec")
    @api.multi
    def _compute_rec(self):
        self.vv = '(%s) Notice No %s u/s %s for Tax Year %s' %(self.client_name.name,self.notice_no,self.section_no ,self.tax_year)
    _rec_name = 'vv'

class RTO(models.Model):
    _name = 'rto.rto'
    rto   = fields.Char('RTO')
    code  = fields.Char('Code')

    _rec_name = 'rto'

class correspondencehistory(models.Model):
    _name = 'correspondence.history'

    hearing_date = fields.Date('Hearing Date',required=True)
    atendee_name = fields.Many2one('hr.employee','Attendee Name', required=True)

    x_type = fields.Selection([
        ('adjournment','Adjournment'),
        ('reply','Reply'),
        ],string="Type")

    nex_hear_dat = fields.Date('Next Hearing Date')          
    remarks      = fields.Text()
    

    attachment =  fields.Binary(string="Attachment")
    @api.multi
    def import_attachment(self):
        fileobj = TemporaryFile('w+')
        fileobj.write(base64.decodestring(attachment))
        return

    correspondence_his = fields.Many2one('correspondence.correspondence',
    ondelete='cascade', string="Name", required=True)
    
    _rec_name = 'correspondence_his'