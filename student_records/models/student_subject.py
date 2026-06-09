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
    _name = 'subject.subject'
    _description = 'Subjects taken by Students'

    subject_name = fields.Char(string='Subject Name', required=True)

    units = fields.Integer(string='Units')
    
    #Connection to the enrollment
    enrollee_id = fields.One2many('student.enrollment', 'subject_id', string ='Enrollees')
   
    enrollee_count = fields.Integer(string='Enrollee Count', compute='_compute_enrollees_count')

    @api.depends('enrollee_id')
    def _compute_enrollees_count(self):
        for record in self:
            record.enrollee_count = len(record.enrollee_id)
            
    