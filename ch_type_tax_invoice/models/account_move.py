# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountMove(models.Model):
    
    _inherit = 'account.move'

    # Dependencies: ต้องคำนวณใหม่เมื่อค่าเหล่านี้เปลี่ยน
    # partner_id, sale_journal_id (partner), purchase_journal_id (partner),
    # move_type, company_id
    @api.depends('partner_id', 'partner_id.sale_journal_id', 'partner_id.purchase_journal_id', 'move_type', 'company_id')
    def _compute_journal_id(self):
        """
        Override เพื่อกำหนด Journal เริ่มต้นตาม Journal เฉพาะของ Partner:
        - sale_journal_id สำหรับเอกสารประเภทขาย (out_invoice, out_refund)
        - purchase_journal_id สำหรับเอกสารประเภทซื้อ (in_invoice, in_refund)
        ถ้า Partner ไม่ได้กำหนดไว้ ให้ใช้ Default Journal ตามประเภทเอกสารนั้นๆ โดยการค้นหา
        """
        # เรียก super() ก่อนเพื่อให้ logic อื่นๆ หรือค่าเริ่มต้นบางอย่างทำงาน
        # ค่าที่ได้จาก super() อาจถูกเขียนทับโดย logic ด้านล่างนี้
        super()._compute_journal_id()

        journal_model = self.env['account.journal'] # Cache model instance ไว้ใช้วน loop

        for move in self:
            # ดึง company_id (ถ้ายังไม่มี ใช้ company ปัจจุบัน)
            company_id = move.company_id.id or self.env.company.id
            # ดึง partner instance
            partner = move.partner_id

            # --- Logic สำหรับประเภทเอกสารขาย ---
            if move.move_type in ('out_invoice', 'out_refund'):
                journal_type_default = 'sale' # ประเภท Journal ปกติสำหรับฝั่งขาย
                specific_journal = partner.sale_journal_id if partner else None

                if specific_journal: # ถ้า Partner มี Sale Journal เฉพาะกำหนดไว้
                    # กำหนด Journal เฉพาะ ถ้าค่าไม่เหมือนเดิม
                    if move.journal_id != specific_journal:
                        move.journal_id = specific_journal
                else: # ถ้า Partner ไม่มี Sale Journal เฉพาะ -> ค้นหา Default Sale Journal
                    domain = [('company_id', '=', company_id), ('type', '=', journal_type_default)]
                    default_journal = journal_model.search(domain, limit=1)
                    # กำหนด Default Journal ที่หาเจอ ถ้าค่าไม่เหมือนเดิม
                    if default_journal and move.journal_id != default_journal:
                        move.journal_id = default_journal
                    # กรณีค้นหา default_journal ไม่เจอ: ปล่อยให้เป็นค่าที่ได้จาก super() หรือ logic อื่น

            # --- Logic สำหรับประเภทเอกสารซื้อ ---
            elif move.move_type in ('in_invoice', 'in_refund'):
                journal_type_default = 'purchase' # ประเภท Journal ปกติสำหรับฝั่งซื้อ
                specific_journal = partner.purchase_journal_id if partner else None

                if specific_journal: # ถ้า Partner มี Purchase Journal เฉพาะกำหนดไว้
                     # กำหนด Journal เฉพาะ ถ้าค่าไม่เหมือนเดิม
                    if move.journal_id != specific_journal:
                        move.journal_id = specific_journal
                else: # ถ้า Partner ไม่มี Purchase Journal เฉพาะ -> ค้นหา Default Purchase Journal
                    domain = [('company_id', '=', company_id), ('type', '=', journal_type_default)]
                    default_journal = journal_model.search(domain, limit=1)
                    # กำหนด Default Journal ที่หาเจอ ถ้าค่าไม่เหมือนเดิม
                    if default_journal and move.journal_id != default_journal:
                        move.journal_id = default_journal
                    # กรณีค้นหา default_journal ไม่เจอ: ปล่อยให้เป็นค่าที่ได้จาก super() หรือ logic อื่น