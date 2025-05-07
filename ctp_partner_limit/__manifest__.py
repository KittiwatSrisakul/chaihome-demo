# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybernetics Plus Co., Ltd.
#    GGM Certificate
#
#    Copyright (C) 2021-TODAY Cybernetics Plus Technologies (<https://www.cybernetics.plus>).
#    Author: Cybernetics Plus Techno Solutions (<https://www.cybernetics.plus>)
#
###################################################################################
{
    "name": "Partner Limit Cost",
    "version": "17.0.1.0.1",
    "summary": "C+ Projects Fields",
    "description": "Partner Limit Cost",
    "author": "Cybernetics+",
    "website": "https://www.cybernetics.plus",
    "live_test_url": "https://www.cybernetics.plus",
    "category": "Customizations",
    "license": "Other proprietary",
    "price": 999999999.99,
    "currency": "EUR",
    "installable": True,
    "application": False,
    "auto_install": False,
    "contributors": [
        "C+ Developer <dev@cybernetics.plus>",
    ],
    "depends": ["base", "contacts", "approvals", "account", "sale"],
    "data": [
        "views/sale_order.xml",
        "views/approve.xml",
        "views/res_config_setting.xml"
    ],
}
