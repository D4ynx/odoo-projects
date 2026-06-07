from odoo import models, fields, api

class StudentSubject(models.Model):
    _name = 'student.subject'
    _description = 'Subjects taken by Students'
    
    subject_name = fields.Char(string='Subject Name', required=True)
    grade = fields.Float(string='Grade')
    units = fields.Integer(string='Units')
    student_id = fields.Many2one('student.record', string='Student', ondelete='cascade')