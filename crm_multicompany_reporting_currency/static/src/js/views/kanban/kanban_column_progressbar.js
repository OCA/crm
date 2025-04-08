odoo.define(
    "crm_multicompany_reporting_currency.kanban_column_progressbar",
    function (require) {
        "use strict";

        const KanbanColumnProgressBar = require("web.KanbanColumnProgressBar");
        const session = require("web.session");

        KanbanColumnProgressBar.include({
            /**
             * Override to replace sum_field options currency_field with current_company_currency.
             * This gives a possibility to change the currency displayed on progressbar
             */
            init: function (parent, options, columnState) {
                this._super.apply(this, arguments);
                var companyCurrency =
                    columnState.progressBarValues.company_currency_field;
                if (companyCurrency && columnState.data.length) {
                    this.currency =
                        session.currencies[
                            columnState.data[0].data[companyCurrency].res_id
                        ];
                }
            },
        });
    }
);
