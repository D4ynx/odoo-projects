{
    'name': 'Student Records',
    'version': '1.0',
    'summary': 'Manage student records and their subjects',
    'description': 'A module to manage student records and the subjects they are taking',
    'author': 'D4ynx',
    'depends': ['base'],
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/student_record_views.xml',
        'views/student_subject_views.xml',
        'views/student_enrollment_views.xml',
        'views/student_semester_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}