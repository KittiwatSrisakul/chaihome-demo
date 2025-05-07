from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('partner_id')
    def _compute_journal_id(self):
        for rec in self:
            if rec.partner_id.sale_journal_id:
                rec.journal_id = rec.partner_id.sale_journal_id
            else:
                self.journal_id = False
