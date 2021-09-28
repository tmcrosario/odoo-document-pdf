from os import path

from odoo import api, fields, models


class Document(models.Model):

    _name = "tmc.document"
    _inherit = "tmc.document"

    pdf_path = fields.Char(compute="_compute_pdf_path_and_url", readonly=True)

    pdf_url = fields.Char(compute="_compute_pdf_path_and_url", readonly=True)

    def get_path_and_url(self):
        res = None
        repository_path = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("tmc.document.repository_path")
        )
        repository_url = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("tmc.document.repository_url")
        )
        file_name = self.name.replace("/", "-") + ".pdf"
        res = {
            "path": repository_path + str(self.period) + "/" + file_name,
            "url": repository_url + str(self.period) + "/" + file_name,
        }

        return res

    @api.depends("document_type_id", "dependence_id", "number", "period")
    def _compute_pdf_path_and_url(self):
        for document in self:
            document.pdf_path = None
            document.pdf_url = None
            res = document.get_path_and_url()
            if res and path.isfile(res["path"]):
                document.pdf_path = res["path"]
                document.pdf_url = res["url"]

    def open_pdf(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": self.pdf_url,
            "target": "new",
        }
