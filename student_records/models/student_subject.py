from odoo import models, fields, api

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
    
class StudentSubject(models.Model):
    _name = 'student.subject'
    _description = 'Subjects taken by Students'

    name = fields.Char(string='Subject Name', required=True)
    course_code = fields.Char(string='Course Code', required=True)
    course = fields.Selection([
        ('computer_science', 'Computer Science'),
        ('information_technology','Information Technology'),
        ('business_administration', 'Business Administration'),
    ])
    units = fields.Integer(string='Units')
    
    #Connection to the enrollment
    enrollee_ids = fields.One2many('student.enrollment', 'subject_id', string ='Enrollees')
   
    enrollee_count = fields.Integer(string='Enrollee Count', compute='_compute_enrollees_count', store=True)

    @api.depends('enrollee_ids')
    def _compute_enrollees_count(self):
        for record in self:
            record.enrollee_count = len(record.enrollee_ids)
            
    