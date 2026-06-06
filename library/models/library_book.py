from odoo import models, fields, api
from datetime import date

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    
    name = fields.Char(string='Title', required=True)
    author_id = fields.Many2one('library.author', string='Author', required=True)
    isbn = fields.Char(string='ISBN')
    date_published = fields.Date(string='Date Published')
    active = fields.Boolean(string='Active', default=True)
    is_featured = fields.Boolean(string='Featured', default=False)
    
    days_since_published = fields.Integer(
        string = 'Days Since Published',
        compute = '_compute_days_since_published'
        )
    
    @api.depends('date_published')
    def _compute_days_since_published(self):    
        for record in self:
            if record.date_published:
                record.days_since_published = (date.today() - record.date_published).days
            else:
                record.days_since_published = 0
                
    def action_feature(self):
        for record in self:
            record.is_featured = True
    
        