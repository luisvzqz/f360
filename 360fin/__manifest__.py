# -*- coding: utf-8 -*-
{
    'name': "360fin",

    'summary': """
        Financial Tool for small / medium financial entities 
        AML, Loans, Accounting, Inventory and more """,

    'description': """
        ERP for small / medium financial entities      
        AML, Loans, Accounting, Inventory and more
    """,

    'author': "mulaWare",
    'website': "https://360fin.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts', 'sale','sale_management','crm', 'product', 'hr','mail'],
    # always loaded
    'data': [
      	  'views/res_partner_view.xml',
          'views/res_company_view.xml',
          'views/product_template_view.xml',
          'views/sale_order_view.xml',
          'views/report_quotation_360fin.xml'
        #  'views/hr_employee_view.xml',
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #    'demo/demo.xml',
    # ],
   "installable": True,
   "auto_install": True,
}
