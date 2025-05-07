from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_approve_credit_limit = fields.Boolean('Approve Credit Limit',
                                             config_parameter='ctp_partner_limit.is_approve_credit_limit')
    approve_credit_select = fields.Selection([('jus_approve', 'Just Approve The Sale'),
                                              ('increase_approve', 'Increase Credit Limit')],
                                             default='', config_parameter='ctp_partner_limit.approve_credit_select')
    # is_jus_approve_limit = fields.Boolean('Just Approve The Sale',
    #                                       readonly=False, compute='_onchange_approve_limit', store=True,
    #                                       config_parameter='ctp_partner_limit.is_jus_approve_limit')
    # is_increase_approve_limit = fields.Boolean('Increase Credit Limit',
    #                                            config_parameter='ctp_partner_limit.is_increase_approve_limit',
    #                                            readonly=False, compute='_onchange_increase_approve_limit', store=True)
    #
    # @api.onchange('is_jus_approve_limit')
    # def _onchange_approve_limit(self):
    #     if self.is_jus_approve_limit:
    #         self.is_increase_approve_limit = False
    #
    # @api.onchange('is_increase_approve_limit')
    # def _onchange_increase_approve_limit(self):
    #     if self.is_increase_approve_limit:
    #         self.is_jus_approve_limit = False