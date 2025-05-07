from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    limit_cost = fields.Float('Limit Cost', default=0.00)
    is_partner_limit = fields.Boolean('Partner Limit', default=False)
    is_partner_limit_not = fields.Boolean('Partner Limit Not Update', default=False)

    def request_to_approve(self):
        approve = self.env['approval.category'].search([('is_partner_limit', '=', True)])
        if approve:
            approve.create_request()
