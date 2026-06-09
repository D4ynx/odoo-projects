from odoo import models, fields, api
from odoo.exceptions import ValidationError

PASSING_GRADES = ['A', 'A-', 'B', 'B-', 'C']

GRADE_POINTS = {
        'A':4.0,
        'A-': 3.5,
        'B' : 3,
        'B-': 2.5,
        'C' : 2,
        'D' : 1.5,
        'F' : 1,
    }

class StudentEnrollment (models.Model):
    _name = 'student.enrollment'
    _description = 'Student specific enrollment details'
    
    #Connection to the student.record
    student_id = fields.Many2one('student.record', string='Student', ondelete='cascade')
    
    #Connection to the student.subject
    subject_id = fields.Many2one('student.subject', string='Subject', ondelete='cascade')
    
    grade = fields.Selection([
        ('A', 'A'),
        ('A-', 'A-'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    ], string='Grade', required=True)
    
    is_passed = fields.Boolean(string='Passed', compute='_compute_is_passed')
    
    @api.depends('grade')
    def _compute_is_passed(self):
        for record in self:
            record.is_passed = record.grade in PASSING_GRADES