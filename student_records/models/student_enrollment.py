from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

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
    student_id = fields.Many2one('student.record', string='Student', default=lambda self: self.env.context.get('default_student_id'))
    
    #Relational Field for subject_id
    student_course = fields.Selection(related='student_id.course', string='Course')
    
    #Connection to the student.subject
    subject_id = fields.Many2one('student.subject', string='Subject', ondelete='cascade', domain="[('course', '=', student_course)]")

    #Connection to student.semester
    enrollment_semester_records = fields.Many2one('student.semester', string='Semester')
        
    academic_year = fields.Char(string='Academic Year')
    
    status = fields.Selection([
        ('ongoing','Ongoing'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    ], readonly = True, compute="_compute_status", default = 'ongoing')
    
    grade = fields.Selection([
        ('A', 'A'),
        ('A-', 'A-'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    ], string='Grade')

    @api.depends('grade')
    def _compute_status(self):
        for record in self:
            if not record.grade:
                record.status = 'ongoing'
            elif record.grade in PASSING_GRADES:
                record.status = 'passed'
            else:
                record.status = 'failed'
                
    @api.onchange('enrollment_semester_records')
    def _onchange_semester_records(self):
        for record in self:
            if self.enrollment_semester_records:
                    self.student_id = self.enrollment_semester_records.semester_student_id
                    
    @api.constrains('student_id', 'subject_id')
    def _check_course_subject(self):
        for record in self:
            if record.subject_id and record.student_id:
                if record.subject_id.course != record.student_id.course:
                    raise ValidationError(
                        f'Subject {record.subject_id.course} does not belong to {record.student_id.course}!'
                    )
                
    @api.model
    def create(self, vals):
        if not vals.get('student_id') and vals.get('enrollment_semester_records'):
            semester = self.env['student.semester'].browse(vals['enrollment_semester_records'])
            if semester.semester_student_id:
                vals['student_id'] = semester.semester_student_id.id
        return super().create(vals)
                
