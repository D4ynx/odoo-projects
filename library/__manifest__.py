{
    'name': 'Library',
    'version': '1.0',
    'summary': 'Manage books in a library',
    'description': 'A simple module to manage books and authors',
    'author': 'D4ynx',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv', 
        'views/library_book_views.xml',
        'views/sequence.xml',
        'views/library_author_views.xml',
        ],
    'installable': True,
    'auto_install': False,
}

