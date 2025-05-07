from odoo import models, fields, _, api


class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    is_partner_limit = fields.Boolean('Partner Limit', default=False)
    is_partner_limit_not = fields.Boolean('Partner Limit Not Update', default=False)

    def create_request(self):
        self.ensure_one()
        # If category uses sequence, set next sequence as name
        # (if not, set category name as default name).
        approve_parameter = (self.env['ir.config_parameter'].get_param('ctp_partner_limit.approve_credit_select'))
        if approve_parameter == 'jus_approve':
            self.write({
                'is_partner_limit': approve_parameter,
            })
        else:
            self.write({
                'is_partner_limit_not': approve_parameter,
            })

        return {
            "type": "ir.actions.act_window",
            "res_model": "approval.request",
            "views": [[False, "form"]],
            "context": {
                'default_name': _('New') if self.automated_sequence else self.name,
                'default_category_id': self.id,
                'default_request_owner_id': self.env.user.id,
                'default_request_status': 'new',
                'default_is_partner_limit': self.is_partner_limit,
                'default_is_partner_limit_not': self.is_partner_limit_not,
            },
        }


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    is_partner_limit = fields.Boolean('Partner Limit', default=False)
    is_partner_limit_not = fields.Boolean('Partner Limit Not Update', default=False)
    credit = fields.Float('Credit', default=0.00, compute='_compute_partner_limit')
    sale_order_id = fields.Many2one('sale.order')

    @api.onchange('partner_id')
    def _compute_partner_limit(self):
        if self.partner_id and self.is_partner_limit and not self.is_partner_limit_not:
            self.credit = self.partner_id.credit_limit
        else:
            self.credit = 0

    def action_approve(self, approver=None):
        res = super().action_approve()
        self._ensure_can_approve()

        if self.is_partner_limit and self.partner_id and not self.is_partner_limit_not:
            self.partner_id.write({
                'credit_limit': self.amount,
            })

        if self.is_partner_limit_not and self.sale_order_id:
            self.sale_order_id.write({
                'approve_req_status': 'approved',
            })

        if not isinstance(approver, models.BaseModel):
            approver = self.mapped('approver_ids').filtered(
                lambda approver: approver.user_id == self.env.user
            )
        approver.write({'status': 'approved'})
        self.sudo()._update_next_approvers('pending', approver, only_next_approver=True)
        self.sudo()._get_user_approval_activities(user=self.env.user).action_feedback()
        return res

    def action_refuse(self, approver=None):
        res = super().action_refuse(approver=approver)
        if self.sale_order_id:
            self.sale_order_id.write({
                'approve_req_status': 'refused',
            })

        return res

    def action_confirm(self):
        res = super().action_confirm()
        if self.sale_order_id:
            self.sale_order_id.write({
                'approve_req_status': 'pending',
                'approve_request_id': self.id,
            })

        return res

    def action_cancel(self):
        res = super().action_cancel()
        if self.sale_order_id:
            self.sale_order_id.write({
                'approve_req_status': 'cancel',
            })

        return res

    def create(self, vals):
        res = super(ApprovalRequest, self).create(vals)
        if vals.get('sale_order_id'):
            sale_order = self.env['sale.order'].browse(vals.get('sale_order_id'))
            sale_order.write({
                'approve_req_status': 'new',
                'approve_request_id': res.id,
            })

        return res