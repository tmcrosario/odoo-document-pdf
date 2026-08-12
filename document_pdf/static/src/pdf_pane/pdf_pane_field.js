/** @odoo-module **/

import {registry} from "@web/core/registry";
import {Component} from "@odoo/owl";
import {standardFieldProps} from "@web/views/fields/standard_field_props";

export class PdfPaneField extends Component {
    static template = "document_pdf.PdfPaneField";
    static props = {...standardFieldProps};

    // #view=Fit asks the browser viewer to show the whole page.
    get pdfSrc() {
        const resId = this.props.record.resId;
        return resId ? `/tmc/document/${resId}/pdf#view=Fit` : false;
    }
}

export const pdfPaneField = {
    component: PdfPaneField,
    supportedTypes: ["char"],
};

registry.category("fields").add("tmc_pdf_pane", pdfPaneField);
