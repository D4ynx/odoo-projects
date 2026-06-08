from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StudentRecord (models.Model):
    _name = 'student.record'
    _description = 'Student Record'
    
    reference = fields.Char(string='Student ID', copy=False, readonly=True, default ='New')
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    course = fields.Selection([
        ('computer_science', 'Computer Science'),
        ('information_technology', 'Information Technology'),
        ('business_administration', 'Business Administration'),    
    ], string = 'Course')
    
    yearlvl = fields.Selection([
        ('first_year', 'First Year'),
        ('second_year', 'Second Year'),
        ('third_year', 'Third Year'),
        ('fourth_year', 'Fourth Year'),
    ], string = 'Year Level')
    
    gpa = fields.Float(string='GPA')
    status = fields.Selection([
        ('enrolled', 'Enrolled'),
        ('graduated', 'Graduated'),
        ('dropped', 'Dropped'),
    ], string = 'Status', default='enrolled')
    
    enrollment_date = fields.Date(string='Enrollment Date')
    
    subject_ids = fields.One2many('student.subject', 'student_id', string = 'Subjects')
    
    @api.constrains('gpa')
    def _check_gpa(self):
        for record in self:
            if record.gpa and (record.gpa < 0.0 or record.gpa > 4.0):
                raise ValidationError('GPA must be between 0.0 and 4.0.')
            
    @api.constrains('enrollment_date')
    def _check_enrollment_date(self):
        for record in self:
            if record.enrollment_date and record.enrollment_date > fields.Date.today():
                raise ValidationError('Enrollment date cannot be in the future.')
    @api.model
    def create(self, vals):
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('student.record')
        return super().create(vals)
    
    def action_graduated(self):
        for record in self:
            record.status = 'graduated'
    
    def action_dropped(self):
        for record in self:
            record.status = 'dropped'
    
    def action_enrolled(self):
        for record in self:
            record.status = 'enrolled'
    
     