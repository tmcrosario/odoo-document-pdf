from os import path
from odoo import api, fields, models


class Document(models.Model):

    _name = 'tmc.document'
    _inherit = 'tmc.document'

    pdf_url = fields.Char(compute='_compute_pdf_url', readonly=True)

    def _get_path_and_url(self):
        try:
            repository_path = self.env['ir.config_parameter'].sudo().get_param(
                'tmc.document.repository_path')
            repository_url = self.env['ir.config_parameter'].sudo().get_param(
                'tmc.document.repository_url')
            file_name = self.name.replace('/', '-') + '.pdf'
            return {
                'file_path': repository_path + file_name,
                'url': repository_url + file_name
            }
        except Exception:
            return None

    @api.depends('document_type_id', 'dependence_id', 'number', 'period')
    def _compute_pdf_url(self):
        for document in self:
            document.pdf_url = None
            res = document._get_path_and_url()
            if res and path.isfile(res['file_path']):
                document.pdf_url = res['url']

    def open_pdf(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.pdf_url,
            'target': 'new',
        }
