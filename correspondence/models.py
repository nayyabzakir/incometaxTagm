# -*- coding: utf-8 -*-

from openerp import models, fields, api

class CorresPrototype(models.Model):
    _name = "corres.corres.prototype"
    client_name    = fields.Many2one('res.partner','Client Name', required=True)
    section_no     = fields.Char('Section No ',required=True)
    section_des    = fields.Char('Section Description')
    acc_officer    = fields.Many2one('corres.acc.officer','Assessing Officer', required=True)
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
    _name                   = 'correspondence.correspondence'

    _inherit                = ['mail.thread', 'ir.needaction_mixin','corres.corres.prototype']

    stages                  = fields.Many2one('correspondence.stage','Stage Name',track_visibility='always')
    stage_name                  = fields.Selection([
                                ('order', 'Order'),
                                ('first_appeal', 'First Appeal'),
                                ('stay', 'Stay'),
                                ('sec_appeal', 'Second Appeal'),
                                ('ref_to_hc', 'Reference to High Court'),
                                ], default="order")

    type_of                 = fields.Many2one('correspondence.type','Type')
    internal_file_no        = fields.Char("Internal File No")
    ntn_no                  = fields.Char("NTN")
    strn_no                 = fields.Char("STRN")
    ao_zone                 = fields.Char('Zone')
    ao_unit                 = fields.Char('Unit')
    ao_designation          = fields.Char('Designation')
    ito_name                = fields.Char("ITO Name")
    ito_contact_no          = fields.Char("ITO Contact No")
    vv                      = fields.Char(compute="_compute_rec")
    @api.multi
    def _compute_rec(self):
        self.vv = '(%s) Notice No %s u/s %s for Tax Year %s' %(self.client_name.name,self.notice_no,self.section_no ,self.tax_year)
    _rec_name = 'vv'


    @api.onchange('client_name')
    def onchangeClientName(self):
        if self.client_name:
            self.ntn_no  = self.client_name.regis_no
            self.strn_no = self.client_name.strn

    @api.onchange('acc_officer')
    def onchangeAccessOfficer(self):
        if self.acc_officer:
            self.ao_zone  = self.acc_officer.ao_zone
            self.ao_unit = self.acc_officer.ao_unit
            self.ao_designation = self.acc_officer.ao_designation
            self.rto = self.acc_officer.rto



#Correspondence Accessing Officer Class
class CorresAccOfficer(models.Model):
    _name = 'corres.acc.officer'
    name                    = fields.Char("Name")
    ao_zone                 = fields.Char('Zone')
    ao_unit                 = fields.Char('Unit')
    ao_designation          = fields.Char('Designation')
    rto                     = fields.Many2one('rto.rto','RTO')

# #Correspondence Zone Class
# class CorrespondenceType(models.Model):
#     _name = 'correspondence.zone'
#     name  = fields.Char("Name")

# #Correspondence Unit Class
# class CorrespondenceType(models.Model):
#     _name = 'correspondence.unit'
#     name  = fields.Char("Name")

# #Correspondence Designation Class
# class CorrespondenceType(models.Model):
#     _name = 'correspondence.designation'
#     name  = fields.Char("Name")



#Correspondence Type Class
class CorrespondenceType(models.Model):
    _name = 'correspondence.type'
    name  = fields.Char("Name")

#Correspondence Stages Class
class CorrespondenceStages(models.Model):
    _name = 'correspondence.stage'
    name  = fields.Char("Name")
    sequence  = fields.Char("Sequence")


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


# RTO Class
class RTO(models.Model):
    _name = 'rto.rto'
    rto   = fields.Char('RTO')
    code  = fields.Char('Code')

    _rec_name = 'rto'


#Correspondence History Class
class correspondencehistory(models.Model):
    _name = 'correspondence.history'

    hearing_date = fields.Date('Hearing Date',required=True)
    atendee_name = fields.Many2one('hr.employee','Attendee Name')

    x_type = fields.Many2one('correspondence.history.type',string="Type")

    nex_hear_dat = fields.Date('Next Hearing Date')          
    remarks      = fields.Text()
    attachment   = fields.Many2one('correspondence.attachment','Attachment')
    acc_officer    = fields.Many2one('corres.acc.officer','Assessing Officer', required=True)
    cor_file_type= fields.Many2one('correspondence.file.type','Reply')
    
    correspondence_his = fields.Many2one('correspondence.correspondence',
    ondelete='cascade', string="Name", required=True)
    
    _rec_name = 'correspondence_his'




#Correspondence History Type Class
class CorrespondenceHistoryType(models.Model):
    _name = 'correspondence.history.type'
    name  = fields.Char("Name")


#Correspondence Attachment Class
class CorrespondenceAttachment(models.Model):
    _name = 'correspondence.attachment'
    attachment_tree_ids = fields.One2many('correspondence.attachment.tree','attachment_id')

#Correspondence Attachment Tree Class
class CorrespondenceAttachmentTree(models.Model):
    _name = 'correspondence.attachment.tree'
    name  = fields.Char("Description")
    attachment =  fields.Binary(string="Attachment")
    attachment_id = fields.Many2one('correspondence.attachment','Attachment')
    @api.multi
    def import_attachment(self):
        fileobj = TemporaryFile('w+')
        fileobj.write(base64.decodestring(attachment))
        return



# Correspondence File Type Class
class correspondencefiletype(models.Model):
    _name = 'correspondence.file.type'
    date = fields.Date('Date')
    assessing_officer = fields.Many2one('corres.acc.officer','Assessing Officer')
    notice_no = fields.Char("Notice No")
    subject = fields.Char("Subject")
    detail = fields.Char("Detail")
    description      = fields.Text()
    customer_name    = fields.Many2one('res.partner','Client')
    state = fields.Selection([
        ('draft','Draft'),
        ('validate','Validated'),
        ],string="Stage", default="draft")

    vv                      = fields.Char(compute="_compute_rec")
    @api.multi
    def _compute_rec(self):
        self.vv = 'Notice No %s dated %s for %s' %(self.notice_no,self.date ,self.customer_name)
    _rec_name = 'vv'

    @api.multi
    def validate(self):
        self.write({'state': 'validate'})