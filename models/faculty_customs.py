from odoo import models, fields, api, _


class FacultyDetails(models.Model):
    _name = "faculty.details"
    _inherit = 'mail.thread'

    name = fields.Many2one('res.users', domain=['|',('faculty_check', '=', True), ('youtube_faculty', '=', True)], string="Name")
    qualification = fields.Char(string="Qualification")
    exp = fields.Char(string="Experience")
    course = fields.Many2many('courses.details', string="Courses")
    # bank_acc = fields.Integer(string="Bank account")
    test = fields.Many2one('res.class', string='Class Room')
    pay_test = fields.Char(string="Pay")
    tds = fields.Char(string="Tds")
    salary_hr = fields.Integer(string="Salary per Hour")
    bank_acc = fields.Many2one('res.partner.bank',
                               string="Bank Account",
                               ondelete='restrict', copy=False, required=True)
    email_address = fields.Char(string="Email")
    date_birth = fields.Date(string='Date of Birth')
    pan_number = fields.Char(string='Pan Number')
    payout_ids = fields.One2many('payout', 'payout_id')
    gst_number = fields.Char(string='Gst Number')
    bank_name = fields.Char('Bank name', required=True)
    account_holder = fields.Char('Account holder name')
    bank_account_no = fields.Char('Bank account number', required=True)
    ifsc = fields.Char('IFSC', required=True)
    user_id = fields.Many2one('res.users', string="Approved By", default=lambda self: self.env.user.id, readonly="1",
                              tracking=True)
    scheduled_ids = fields.One2many('scheduled.classes', 'schedule_id')
    date_month = fields.Selection([
        ('january', 'January'), ('february', 'February'),
        ('march', 'March'), ('april', 'April'),
        ('may', 'May'), ('june', 'June'), ('july', 'July'), ('august', 'August'),
        ('september', 'September'), ('october', 'October'), ('november', 'November'),
        ('december', 'December')],
        string='Month of Birth', copy=False,
        tracking=True)
    current_status = fields.Selection([
        ('active', 'Active'), ('inactive', 'Inactive')], string='Current status', default='active')
    inactive_date = fields.Date(string='Inactive date')
    gst_status = fields.Boolean('Gst status')
    is_it_changed_faculty = fields.Boolean('Changed Faculty')

    @api.onchange('date_birth')
    def _onchange_date_birth(self):
        print(self.name.name, "this user")
        if self.date_birth != False:
            if self.date_birth.month == 1:
                self.date_month = 'january'
            elif self.date_birth.month == 2:
                self.date_month = 'february'
            elif self.date_birth.month == 3:
                self.date_month = 'march'
            elif self.date_birth.month == 4:
                self.date_month = 'april'
            elif self.date_birth.month == 5:
                self.date_month = 'may'
            elif self.date_birth.month == 6:
                self.date_month = 'june'
            elif self.date_birth.month == 7:
                self.date_month = 'july'
            elif self.date_birth.month == 8:
                self.date_month = 'august'
            elif self.date_birth.month == 9:
                self.date_month = 'september'
            elif self.date_birth.month == 10:
                self.date_month = 'october'
            elif self.date_birth.month == 11:
                self.date_month = 'november'
            elif self.date_birth.month == 12:
                self.date_month = 'december'
            else:
                print("not match")
        else:
            print("ok")


class Courses(models.Model):
    _name = 'courses.details'
    _inherit = 'mail.thread'
    _description = 'Courses'

    name = fields.Char(string='Course Name', required=True)
    subject_ids = fields.Many2many('subject.details', string='Subject', ondelete='restrict')
    # department = fields.Many2one('primary.department', string='Primary department', required=True)

    current_id = fields.Integer()
    used_count = fields.Integer()

    # def action_check_count(self):
    #     rec = self.env['daily.class.record'].sudo().search_count([('course_id', '=', self.id)])
    #     for j in self:
    #         j.used_count = rec
    #
    #     print(rec, "count")

    def add_subject(self):
        # self.state = 'confirm'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'subject.details',
            'view_type': 'form',
            'view_mode': 'form,tree',
        }
        # self.current_id = self.id
        # print("current id", self.id)


class SubjectDetails(models.Model):
    _name = 'subject.details'
    _inherit = 'mail.thread'
    _description = 'Subject'

    name = fields.Char(string='Subject Name', ondelete='restrict', required=True)
    stnd_hr = fields.Float(string='Standard Hours', required=True)
    rec_id = fields.Integer()
    course_sub_id = fields.Many2one('courses.details', string='Course', required=True)
    old_ids = fields.One2many('old.standard.hours', 'old_id', compute='old_standard_hr', store=True)
    change_faculty = fields.Boolean()
    # used_count = fields.Integer()

    # def action_check_count(self):
    #     rec = self.env['daily.class.record'].sudo().search_count([('subject_id', '=', self.id)])
    #     self.used_count = rec
    #     print(rec, "count")

    # @api.model
    # def create(self, vals):
    #     new = []
    #     datas = {
    #         'name': self.name,
    #     }
    #     new.append((0, 0, datas))
    #     self.env['subject.details'].create({
    #         'old_ids': new,
    #     }
    #     )
    #     return super(SubjectDetails, self).create(vals)

    @api.depends('stnd_hr')
    def old_standard_hr(self):
        new = []
        datas = {
            'old_hr': self.stnd_hr,
            'date_update': self.create_date,
            'name': self.env.user.name
        }
        new.append((0, 0, datas))
        self.old_ids = new

    # @api.onchange('name')
    # def _onchange_name(self):
    #     self.env['courses.details'].search([])
    #     self.rec_id = self.id
    #     print(self.rec_id, 'record')


class OldStandardHours(models.Model):
    _name = 'old.standard.hours'
    _inherit = 'mail.thread'

    old_hr = fields.Float(string='Old Standard Hours')
    date_update = fields.Date(string='Update Date')
    name = fields.Char(string='Name')
    old_id = fields.Many2one('subject.details', string='old standard hours')


class ScheduledClasses(models.Model):
    _name = 'scheduled.classes'
    _description = 'Scheduled classes'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string='Date', required=True)
    day = fields.Char(string='Day')
    time_from = fields.Float(string='Time From', widget='time')
    time_to = fields.Float(string='Time To', widget='time')
    faculty_id = fields.Many2one('res.users', string='Faculty', domain=[('faculty_check', '=', True)])
    subject_id = fields.Many2one('subject.details', string='Subject')
    record_id = fields.Integer()

    schedule_id = fields.Many2one('faculty.details', string='Scheduled Classes')


class ChangedStandardHours(models.Model):
    _name = 'changed.standard.hours'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Changed Faculty'
    _rec_name = 'faculty_id'

    date_update = fields.Datetime(string='Update Date')
    faculty_id = fields.Many2one('faculty.details', string='Faculty')
    subject_id = fields.Many2one('subject.details', string='Subject')
    course_id = fields.Many2one('courses.details', string='Course')
    standard_hour = fields.Float(string='Standard Hours')
    old_standard_hour = fields.Float(string='Old Standard Hours')
    coordinator_id = fields.Many2one('res.users', string='Changed by')
