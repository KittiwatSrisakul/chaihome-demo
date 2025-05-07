# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybernetics Plus Co., Ltd.
#    Postgres Query from Odoo Interface
#
#    Copyright (C) 2021-TODAY Cybernetics Plus Technologies (<https://www.cybernetics.plus>).
#    Author: Cybernetics Plus Techno Solutions (<https://www.cybernetics.plus>)
#
###################################################################################

{
    "name": "PostgreSQL Query",
    "version": "17.0.1.0.1",
    "summary": """ 
            Postgres Query from Odoo Interface
            .""",
    "description": """ 
            Postgres Query from Odoo Interface
            .""",
    "author": "Cybernetics+",
    "website": "https://www.cybernetics.plus",
    "live_test_url": "https://www.cybernetics.plus",
    "images": ["static/description/banner.gif"],
    "category": "Base",
    "license": "AGPL-3",
    "price": 999.99,
    "currency": "EUR",
    "application": True,
    "installable": True,
    "auto_install": False,
    "contributors": [
        "C+ Developer <dev@cybernetics.plus>",
    ],
    "depends": ["base", "mail"],
    "data": [
        "datas/data.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/ctp_query_views.xml",
        "wizard/pdforientation.xml",
        # "report/print_pdf.xml",
    ],
}
