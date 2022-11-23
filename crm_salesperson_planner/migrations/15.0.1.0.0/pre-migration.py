from openupgradelib import openupgrade

field_spec = [
    (
        "crm.salesperson.planner.visit.template",
        "crm_salesperson_planner_visit_template",
        "start_datetime",
        "start",
    ),
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
    openupgrade.rename_fields(env, field_spec, False)
