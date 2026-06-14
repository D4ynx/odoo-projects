from odoo import models, api, fields

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

class StudentSemester (models.Model):
    _name = 'student.semester'
    _description = 'Student Enrollment per Semester'
    _order = 'semester_enrollment_yearlvl, semester'
    #Connection to student.record
    semester_student_id = fields.Many2one('student.record', string='Student', ondelete='cascade', default=lambda self: self.env.context.get('default_semester_student_id'))
    
    #Relation connection to student.record course
    semester_student_course = fields.Selection(related='semester_student_id.course', string="Course")
    
    #Connection to student.enrollment
    semester_enrollment_ids = fields.One2many('student.enrollment', 'enrollment_semester_records', string='Enrollments')
    
    semester_enrollment_yearlvl = fields.Selection([
        ('first_year', 'First Year'),
        ('second_year', 'Second Year'),
        ('third_year', 'Third Year'),
        ('fourth_year', 'Fourth Year'),
    ], string="Year Level")
    
    semester = fields.Selection([
        ('first', 'First Semester'),
        ('second', 'Second Semester'),
        ('summer', 'Intersession'),
    ], string = 'Semester')
    

    
    #gpa calculation
    semestral_gpa = fields.Float(compute='_compute_semestral_gpa', string='Semestral GPA', readonly = True, store = True)
    total_units = fields.Integer(string='Total Units', compute='_compute_semestral_gpa', store=True, readonly=True)
    units_passed = fields.Integer(string='Units Passed', compute='_compute_semestral_gpa', store=True, readonly=True)
    subject_count = fields.Integer(string='Subject Count', compute='_compute_semestral_gpa', store=True)
    
    @api.depends('semester_enrollment_ids.grade', 'semester_enrollment_ids.subject_id.units')
    def _compute_semestral_gpa(self):
        for record in self:
            enrollments = record.semester_enrollment_ids
            record.subject_count = len(enrollments)
            record.total_units = sum(e.subject_id.units for e in enrollments)
            passed = enrollments.filtered(lambda e: e.grade in PASSING_GRADES)
            record.units_passed = sum(passed.mapped('subject_id.units'))
            if record.total_units > 0:
                weighted_points = sum(GRADE_POINTS.get(e.grade, 0.0) * e.subject_id.units for e in enrollments)
                record.semestral_gpa = weighted_points / record.total_units
            else:
                record.semestral_gpa = 0.0
                
    @api.onchange('semester_student_id')
    def _onchange_set_yearlvl(self):
        for record in self:
            if record.semester_student_id:
                record.semester_enrollment_yearlvl = record.semester_student_id.student_yearlvl                
    
    @api.model
    def create(self, vals):
        if not vals.get('semester_student_id') and self.env.context.get('default_semester_student_id'):
            vals['semester_student_id'] = self.env.context.get('default_semester_student_id')
        return super().create(vals)
    
    
    
    