from odoo import models, fields, api
import json


class ResPartner(models.Model):
    _inherit = 'res.partner'

    current_company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    sale_journal_id = fields.Many2one('account.journal', string='Sales Journal',
                                      domain="[('type', '=', 'sale'), ('company_id', '=', current_company_id)]",
                                      compute='_compute_sale_journal')
    purchase_journal_id = fields.Many2one('account.journal', string='Purchase Journal',
                                          domain="[('type', '=', 'purchase'), ('company_id', '=', current_company_id)]",
                                          compute='_compute_purchase_journal')
    company_sale_journal_map = fields.Text(string='Sale Journal Map', default='{}')
    company_purchase_journal_map = fields.Text(string='Purchase Journal Map', default='{}')

    def _compute_sale_journal(self):
        for rec in self:
            sale_map = json.loads(rec.company_sale_journal_map or '{}')
            current_company_id = str(self.env.company.id)
            main_company_sale_journal = sale_map.get('main_company', {}).get(current_company_id)
            secondary_company_sale_journal = sale_map.get('secondary_company', {}).get(current_company_id)

            if self.env.company.id == 1:
                if main_company_sale_journal:
                    rec.sale_journal_id = main_company_sale_journal
                else:
                    rec.sale_journal_id = False
            else:
                if secondary_company_sale_journal:
                    rec.sale_journal_id = secondary_company_sale_journal
                else:
                    rec.sale_journal_id = False

    def _compute_purchase_journal(self):
        for rec in self:
            purchase_map = json.loads(rec.company_purchase_journal_map or '{}')
            current_company_id = str(self.env.company.id)
            main_company_purchase_journal = purchase_map.get('main_company', {}).get(current_company_id)
            secondary_company_purchase_journal = purchase_map.get('secondary_company', {}).get(current_company_id)

            if self.env.company.id == 1:
                if main_company_purchase_journal:
                    rec.purchase_journal_id = main_company_purchase_journal
                else:
                    rec.purchase_journal_id = False
            else:
                if secondary_company_purchase_journal:
                    rec.purchase_journal_id = secondary_company_purchase_journal
                else:
                    rec.purchase_journal_id = False

    @api.onchange('sale_journal_id')
    def _onchange_sale_journal(self):
        for rec in self:
            sale_map = json.loads(rec.company_sale_journal_map or '{}')

            if self.env.company == self.env.user.company_id:
                sale_map['main_company'] = {str(self.env.company.id): rec.sale_journal_id.id}
            else:
                company_id = str(self.env.company.id)
                if 'secondary_company' not in sale_map:
                    sale_map['secondary_company'] = {}
                sale_map['secondary_company'][company_id] = rec.sale_journal_id.id

            rec.company_sale_journal_map = json.dumps(sale_map)

    @api.onchange('purchase_journal_id')
    def _onchange_purchase_journal(self):
        for rec in self:
            purchase_map = json.loads(rec.company_purchase_journal_map or '{}')

            if self.env.company == self.env.user.company_id:
                purchase_map['main_company'] = {str(self.env.company.id): rec.purchase_journal_id.id}
            else:
                company_id = str(self.env.company.id)
                if 'secondary_company' not in purchase_map:
                    purchase_map['secondary_company'] = {}
                purchase_map['secondary_company'][company_id] = rec.purchase_journal_id.id

            rec.company_purchase_journal_map = json.dumps(purchase_map)
