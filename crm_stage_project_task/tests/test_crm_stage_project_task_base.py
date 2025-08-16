from odoo.tests import TransactionCase


class TestCrmStageProjectTaskCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        res_users_obj = cls.env["res.users"].with_context(no_reset_password=True)

        cls.user_saleown = res_users_obj.create(
            {
                "name": "User Bob",
                "login": "bob",
                "email": "bob@example.com",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            cls.env.ref("base.group_user").id,
                            cls.env.ref("sales_team.group_sale_salesman").id,
                        ],
                    )
                ],
            }
        )
        cls.partner_project = cls.env["res.partner"].create(
            {"name": "Valid Partner", "email": "valid.partner@exmaple.com"}
        )

        cls.project_default = (
            cls.env["project.project"]
            .with_context(mail_create_nolog=True)
            .create(
                {
                    "name": "Default",
                    "privacy_visibility": "followers",
                    "partner_id": cls.partner_project.id,
                }
            )
        )
