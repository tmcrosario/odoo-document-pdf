import os

from odoo import api, fields, models


class Document(models.Model):
    _inherit = "tmc.document"

    pdf_url = fields.Char(compute="_compute_pdf_path_and_url", readonly=True)

    # Off-request flag (see _cron_refresh_has_pdf); keeps list render FS-free
    has_pdf = fields.Boolean(default=False)

    def get_path_and_url(self):
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
        # Params are unset on fresh/dev DBs; degrade to no URL instead of TypeError
        if not (repository_path and repository_url and self.name and self.period):
            return None
        file_name = self.name.replace("/", "-") + ".pdf"
        return {
            "path": repository_path + str(self.period) + "/" + file_name,
            "url": repository_url + str(self.period) + "/" + file_name,
        }

    @api.depends("document_type_id", "dependence_id", "number", "period")
    def _compute_pdf_path_and_url(self):
        for document in self:
            document.pdf_url = None
            res = document.get_path_and_url()
            if res and os.path.isfile(res["path"]):
                document.pdf_url = res["url"]

    @api.model
    def _cron_refresh_has_pdf(self):
        base_path = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("tmc.document.repository_path")
        )
        if not base_path:
            return
        self.env.cr.execute(
            "SELECT DISTINCT period FROM tmc_document WHERE period IS NOT NULL"
        )
        for (period,) in self.env.cr.fetchall():
            folder = base_path + str(period) + "/"
            # One readdir per period off-request instead of a stat per row
            try:
                names = set(os.listdir(folder))
            except FileNotFoundError:
                # Period folder not created yet: no PDFs for it
                names = set()
            except OSError:
                # Mount/IO blip: skip so it does not clear every flag
                continue
            docs = self.search([("period", "=", period)])
            to_true, to_false = [], []
            for doc in docs:
                fname = (doc.name or "").replace("/", "-") + ".pdf"
                want = fname in names
                if want != doc.has_pdf:
                    (to_true if want else to_false).append(doc.id)
            if to_true:
                self.browse(to_true).write({"has_pdf": True})
            if to_false:
                self.browse(to_false).write({"has_pdf": False})
            # Bound memory at 200k scale: drop the per-period recordset cache
            self.env.invalidate_all()

    def open_pdf(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": self.pdf_url,
            "target": "new",
        }
