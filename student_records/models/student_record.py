from odoo import models, fields, api
from odoo.exceptions import ValidationError

GRADE_POINTS = {
        'A':4.0,
        'A-': 3.5,
        'B' : 3,
        'B-': 2.5,
        'C' : 2,
        'D' : 1.5,
        'F' : 1,
    }

PASSING_GRADES = ['A', 'A-', 'B', 'B-', 'C']

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
    
    gpa = fields.Float(string='GPA', compute="_compute_gpa", store=True, readonly=True)
    total_units = fields.Integer(string='Total Units', compute='_compute_gpa', store=True, readonly=True)
    units_passed = fields.Integer(string='Units Passed', compute='_compute_gpa', store=True, readonly=True)
    subject_count = fields.Integer(string='Subject Count', compute='_compute_gpa', store=True)
    
    
    status = fields.Selection([
        ('enrolled', 'Enrolled'),
        ('graduated', 'Graduated'),
        ('dropped', 'Dropped'),
    ], string = 'Status', default='enrolled')
    
    enrollment_date = fields.Date(string='Enrollment Date')
    
    #Connection to the student.enrollment
    enrollment_ids = fields.One2many('student.enrollment', 'student_id', string = 'Enrollments')
            
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
    
    
    @api.depends('enrollment_ids.grade', 'enrollment_ids.subject.id_units')
    def _compute_gpa(self):
        for record in self:
            enrollments = record.enrollment_ids
            record.subject_count = len(enrollments)
            record.total_units = sum(e.subject_ids.units for e in enrollments)
            record.units_passed = sum(e.subject_ids.units for e in enrollments if e.grade in PASSING_GRADES)
            if record.total_units > 0:
                weighted_points = sum(GRADE_POINTS.get(e.grade, 0.0) * e.subject_id.units for e in enrollments)
                record.gpa = weighted_points / record.total_units
            else:
                record.gpa = 0.0
        
    
     