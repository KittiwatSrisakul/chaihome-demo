from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    credit = fields.Float('Total Receivable', default=0.0)
    credit_limit = fields.Float('Credit Limit', default=0.0, compute='_compute_credit_limit')
    use_partner_credit_limit = fields.Boolean(default=False, compute='_compute_use_partner_credit_limit')
    approve_req_status = fields.Selection([
        ('new', 'To Submit'),
        ('pending', 'Submitted'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('cancel', 'Cancel'),
    ], default='', copy=False)
    approve_request_id = fields.Many2one('approval.request', copy=False)
    is_credit_limit = fields.Boolean(compute='_compute_is_credit_limit')
    approve_req_ids = fields.One2many('approval.request', inverse_name='sale_order_id')
    count_approve = fields.Integer(compute='_compute_count_approve')

    @api.depends('approve_req_ids')
    def _compute_count_approve(self):
        for rec in self:
            if rec.approve_req_ids:
                rec.count_approve = len(rec.approve_req_ids.ids)
            else:
                rec.count_approve = 0

    @api.depends('credit', 'amount_total', 'credit_limit')
    def _compute_is_credit_limit(self):
        for rec in self:
            if rec.credit + rec.amount_total > rec.credit_limit:
                rec.is_credit_limit = True
            else:
                rec.is_credit_limit = False

    @api.onchange('partner_id')
    def _compute_use_partner_credit_limit(self):
        for rec in self:
            if rec.partner_id.use_partner_credit_limit:
                rec.use_partner_credit_limit = True
            else:
                rec.use_partner_credit_limit = False

    @api.onchange('partner_id')
    def _compute_credit_limit(self):
        for rec in self:
            if rec.partner_id.credit:
                rec.credit = rec.partner_id.credit
            if rec.partner_id.credit_limit:
                rec.credit_limit = rec.partner_id.credit_limit
            else:
                rec.credit = 0
                rec.credit_limit = 0

    def action_create_credit_limit_approve(self):
        # is_jus_approve_limit = self.env['ir.config_parameter'].get_param('ctp_partner_limit.is_jus_approve_limit')
        # is_increase_approve_limit = (self.env['ir.config_parameter']
        #                              .get_param('ctp_partner_limit.is_increase_approve_limit'))
        get_approve_param = (self.env['ir.config_parameter'].get_param('ctp_partner_limit.approve_credit_select'))
        if get_approve_param == 'jus_approve':
            approve = self.env['approval.category'].search([('is_partner_limit_not', '!=', False)], limit=1)

            if approve:
                action = {
                    'res_model': 'approval.request',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'context': {
                        'default_name': approve.name,
                        'default_category_id': approve.id,
                        'default_partner_id': self.partner_id.id,
                        'default_request_owner_id': self.env.user.id,
                        'default_request_status': 'new',
                        'default_reference': self.name,
                        'default_sale_order_id': self.id,
                        'default_is_partner_limit': approve.is_partner_limit if approve.is_partner_limit else False,
                        'default_is_partner_limit_not': approve.is_partner_limit_not
                        if approve.is_partner_limit_not else False,
                    }
                }
                return action

        else:
            approve = self.env['approval.category'].search([('is_partner_limit', '!=', False)], limit=1)

            if approve:
                action = {
                    'res_model': 'approval.request',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'context': {
                        'default_name': approve.name,
                        'default_category_id': approve.id,
                        'default_partner_id': self.partner_id.id,
                        'default_request_owner_id': self.env.user.id,
                        'default_request_status': 'new',
                        'default_reference': self.name,
                        'default_sale_order_id': self.id,
                        'default_is_partner_limit': approve.is_partner_limit if approve.is_partner_limit else False,
                        'default_is_partner_limit_not': approve.is_partner_limit_not
                        if approve.is_partner_limit_not else False,
                    }
                }
                return action

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        # is_jus_approve_limit = self.env['ir.config_parameter'].get_param('ctp_partner_limit.is_jus_approve_limit')
        # is_increase_approve_limit = (self.env['ir.config_parameter']
        #                              .get_param('ctp_partner_limit.is_increase_approve_limit'))
        for rec in self:
            # if is_increase_approve_limit:
            #     if (rec.credit + rec.amount_total > rec.credit_limit):
            #         raise UserError(_("This item cannot be confirmed because over credit limit"))
            # if is_jus_approve_limit:
            if rec.credit + rec.amount_total > rec.credit_limit and rec.approve_req_status != 'approved':
                raise UserError(_("This item cannot be confirmed because over credit limit"))

        return res

    def action_view_approvals(self):
        self.ensure_one()
        action = {
            'res_model': 'approval.request',
            'type': 'ir.actions.act_window',
        }

        if len(self.approve_req_ids.ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.approve_req_ids.ids[0],
            })
        else:
            action.update({
                'name': _("Approvals from %s", self.name),
                'domain': [('id', 'in', self.approve_req_ids.ids)],
                'view_mode': 'tree,form',
            })

        return action
