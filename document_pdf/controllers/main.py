import os

from odoo import http
from odoo.http import request


class DocumentPdfController(http.Controller):
    @http.route("/tmc/document/<int:doc_id>/pdf", type="http", auth="user")
    def tmc_document_pdf(self, doc_id, **kwargs):
        document = request.env["tmc.document"].browse(doc_id).exists()
        if not document:
            return request.not_found()
        document.check_access("read")
        res = document.get_path_and_url()
        if not res or not os.path.isfile(res["path"]):
            return request.not_found()
        with open(res["path"], "rb") as pdf:
            data = pdf.read()
        filename = os.path.basename(res["path"])
        headers = [
            ("Content-Type", "application/pdf"),
            ("Content-Disposition", f'inline; filename="{filename}"'),
        ]
        return request.make_response(data, headers)
