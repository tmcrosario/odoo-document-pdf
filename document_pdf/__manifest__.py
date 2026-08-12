{
    "name": "TMC Document PDF",
    "version": "19.0.1.0.2",
    "summary": "Fields and functions for view documents in PDF",
    "author": "Tribunal Municipal de Cuentas - Municipalidad de Rosario",
    "website": "https://www.tmcrosario.gob.ar",
    "license": "AGPL-3",
    "sequence": 150,
    "depends": ["tmc", "tmc_data"],
    "data": [
        "data/document_cron.xml",
        "views/document_views.xml",
    ],
    "demo": [
        "demo/document_pdf_demo.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "document_pdf/static/src/pdf_pane/pdf_pane_field.js",
            "document_pdf/static/src/pdf_pane/pdf_pane_field.xml",
            "document_pdf/static/src/pdf_pane/pdf_pane_field.scss",
        ],
    },
    "installable": True,
    "application": True,
}  # yapf: disable
