# Migration Notes — odoo-document-pdf (14.0 → 19.0)

Repo contains one module: `document_pdf`.

## Summary of changes by category

### Models

- No changes required. `document_pdf/models/document.py` already uses the modern API
  (`fields.*`, `@api.depends`, `self.env[...]`). No `name_get`, `fields_view_get`,
  `_translate`, `view_type`, `read_group`, `xmlid_to_res_id`, `_sql_constraints`,
  `track_visibility`, `@api.onchange`, `create` override, or bare `_cr/_uid/_context`
  usages found.

### Views

- `document_pdf/views/document_views.xml`: converted three deprecated `attrs` (removed
  in 17.0). All three were the identical single-tuple `= False` invisibility check on
  the `pdf_url` field:
  - `attrs="{'invisible': [('pdf_url', '=', False)]}"` → `invisible="not pdf_url"`
  - One on the form-view stat button (`document_view_form`), two on per-row list buttons
    (`document_view_tree`, `document_simple_view_tree`).
  - These three buttons are per-record action buttons inserted via `position="before"`
    into inherited views; `invisible` (not `column_invisible`) is correct — they are
    buttons, not column-hiding field nodes.
- The file patches inherited views by `ref`; it contains no literal `<tree>`/`<list>`
  tags, no `view_mode`, no `t-esc`, no `oe_chatter`, no `assets_backend`. The record
  ids `document_view_tree` / `document_simple_view_tree` contain `_tree` but were left
  unchanged per the spec (renaming xmlids risks dangling cross-module refs).

### Security

- No security/ files in this repo.

### Tests

- None present.

### Manifests

- `document_pdf`: version `14.0.1.0.0` → `19.0.1.0.0`. `license` already `AGPL-3`,
  `installable` already `True`. No dead `"qweb": []` key. `depends` kept as
  `["tmc", "tmc_data"]` per repo notes. `application: True` left unchanged.

## 18.0 branch

- An 18.0 branch existed but was a pointer-only copy of 14.0 (empty diff) — ignored per
  repo instructions. Branch `19.0` created fresh from `14.0`.

## Removed dependencies

- None removed.

## Dependencies to verify before push

- `tmc` and `tmc_data` — TMC private modules (migrated separately in the odoo-tmc repo);
  verify their 19.0 versions are available before deploy.

## attrs conversions to review

- None compound. All three were the same single-tuple `('pdf_url','=',False)` →
  `not pdf_url` (truthiness on a Char field), which is straightforward.

## Autosave / onchange → constrains conversions

- None. The repo has no `@api.onchange` methods.

## Items left for human review

- None.

## Lint findings

- (captured after pre-commit run below)

## Translations

- Translation regeneration deferred to a later stage.
</content>
</invoke>
