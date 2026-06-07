from odoo import models, fields, api

class StudentRecord (models.Model):
    _name = 'student.record'
    _description = 'Student Record'
    
    reference = fields.Char(string='Student ID', copy=False, required=True, default = 'New')
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