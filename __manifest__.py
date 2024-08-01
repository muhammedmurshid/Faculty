{
    'name': "Faculty",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['mail', 'base', 'crm', 'ohrms_salary_advance'],
    'data': [

        'security/security.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/faculty_details_views.xml',
        'views/classroom_view.xml',
        # 'views/department_main.xml',
        'views/user_checking.xml',
        'views/advance.xml',
        'views/payout.xml',
        'views/department.xml',
        'views/payment_total.xml',
        'views/daily_class_record.xml',
        'views/changed_faculty.xml',
        'views/server_action.xml',
        'views/payment_reject_reason.xml',
        'data/activity.xml',
        'views/youtube_fac_rate.xml',
        'views/youtube_class_record.xml',
        'views/configuration.xml',
        'views/lock_day.xml',
        'views/faculty_payslip.xml',
        'data/server_action.xml',
        'views/crash_class_record.xml',
        'views/faculty_report.xml'

    ],
    'demo': [],
    'summary': "custom_addons_faculty",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}
