from odoo import models, fields, api

class StudentRecord (models.Model):
    _name = 'student.record'
    _description = 'Student Record'
    
    student_id = fields.Char(string='Student ID', copy=False, required=True, default = 'New')
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    course = fields.Selection([
        ('computerScience', 'Computer Science'),
        ('informationTechnology', 'Information Technology'),
        ('BusinessAdministration', 'Business Administration'),    
    ], string = 'Course')
    
    yearlvl = fields.Selection([
        ('firstYear', 'First Year'),
        ('secondYear', 'Second Year'),
        ('thirdYear', 'Third Year'),
        ('fourthYear', 'Fourth Year'),
    ], string = 'Year Level')
    
    gpa = fields.Float(string='GPA')
    status = fields.Selection([
        ('enrolled', 'Enrolled'),
        ('graduated', 'Graduated'),
        ('dropped', 'Dropped'),
    ], string = 'Status')
    
    enrollment_date = fields.Date(string='Enrollment Date')
    
    subject_ids = fields.One2many('student.subject', 'student_id', string = 'Subjects')