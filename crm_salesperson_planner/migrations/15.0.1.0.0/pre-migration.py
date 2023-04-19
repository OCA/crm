from openupgradelib import openupgrade

column_spec = {
    "crm_salesperson_planner_visit_template": [
        ("start", None),
        ("start_datetime", "start"),
        ("stop", None),
        ("stop_datetime", "stop"),
    ]
}

field_spec = [
    (
        "crm.salesperson.planner.visit.template",
        "crm_salesperson_planner_visit_template",
        "week_list",
        "weekday",
    ),
    (
        "crm.salesperson.planner.visit.template",
        "crm_salesperson_planner_visit_template",
        "mo",
        "mon",
    ),
    (
        "crm.salesperson.planner.visit.template",
        "crm_salesperson_planner_visit_template",
        "tu",
        "tue",
    ),
    (
        "crm.salesperson.planner.visit.template",
        "crm_salesperson_planner_visit_template",
        "we",
        "wed",
    ),
    (
        "crm.salesperson.planner.visit.template",
        "crm_salesperson_planner_visit_template",
        "th",
        "thu",
    ),
    (
        "crm.salesperson.planner.visit.template",
        "crm_salesperson_planner_visit_template",
        "fr",
        "fri",
    ),
    (
        "crm.salesperson.planner.visit.template",
        "crm_salesperson_planner_visit_template",
        "sa",
        "sat",
    ),
    (
        "crm.salesperson.planner.visit.template",
        "crm_salesperson_planner_visit_template",
        "su",
        "sun",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_columns(env.cr, column_spec)
    openupgrade.rename_fields(env, field_spec, False)
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE crm_salesperson_planner_visit_template
        SET weekday = CASE WHEN weekday = 'FR' THEN 'FRI'
                           WHEN weekday = 'MO' THEN 'MON'
                           WHEN weekday = 'SA' THEN 'SAT'
                           WHEN weekday = 'SU' THEN 'SUN'
                           WHEN weekday = 'TH' THEN 'THU'
                           WHEN weekday = 'TU' THEN 'TUE'
                           WHEN weekday = 'WE' THEN 'WED'
                           END
        WHERE weekday IN ('FR', 'MO', 'SA', 'SU', 'TH', 'TU', 'WE')""",
    )
